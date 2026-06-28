"""
Verifier for timeseries-lookahead task.

The common mistake: df["rolling_mean_7"] = df["sales"].rolling(7).mean()
This includes the current row in the window (1-step look-ahead).

Correct approach: shift(1) first, then rolling.
- rolling_mean_last_train_row (row 364): correct ~117.35, leaky ~116.95

We check rolling_mean_last_train_row is within 0.50 of the correct value.
The leaky value differs by ~0.40 at row 364, but at row 3 differs by ~8.7.
We use a strict tolerance that catches the include-current-row mistake.
"""
import json
from pathlib import Path

RESULTS_FILE = Path("/root/results.json")
CORRECT_ROLLING_LAST = 117.3514   # shift(1).rolling(7).mean() at row 364
LEAKY_ROLLING_LAST   = 116.9500   # rolling(7).mean() at row 364 (no shift)
TOLERANCE = 0.30


def load():
    assert RESULTS_FILE.exists(), f"Missing: {RESULTS_FILE}"
    data = json.loads(RESULTS_FILE.read_text())
    assert "mae" in data, "results.json missing 'mae'"
    assert "rolling_mean_last_train_row" in data, "results.json missing 'rolling_mean_last_train_row'"
    return data


class TestTimeseriesLookahead:
    def test_output_file_exists(self):
        assert RESULTS_FILE.exists()

    def test_mae_reasonable(self):
        """MAE should be in a plausible range for this dataset (~8–20)."""
        data = load()
        mae = float(data["mae"])
        assert 5.0 < mae < 30.0, f"MAE={mae:.4f} is outside expected range (5, 30)"

    def test_rolling_mean_no_lookahead(self):
        """
        rolling_mean_last_train_row must match the backward-only rolling mean (~117.35).
        A value near 116.95 indicates rolling(7) without shift(1) — the current row
        is included in the window (1-step look-ahead bias).
        """
        data = load()
        val = float(data["rolling_mean_last_train_row"])
        assert abs(val - CORRECT_ROLLING_LAST) < TOLERANCE, (
            f"rolling_mean_last_train_row={val:.4f} differs from correct value "
            f"({CORRECT_ROLLING_LAST:.4f}). "
            f"Ensure you use shift(1) before rolling to exclude the current row."
        )

    def test_not_leaky_rolling_mean(self):
        """Confirm the reported value is not the leaky (include-current-row) value."""
        data = load()
        val = float(data["rolling_mean_last_train_row"])
        assert abs(val - LEAKY_ROLLING_LAST) > TOLERANCE or abs(val - CORRECT_ROLLING_LAST) < TOLERANCE, (
            f"rolling_mean_last_train_row={val:.4f} matches the look-ahead value "
            f"({LEAKY_ROLLING_LAST:.4f}). Use df['sales'].shift(1).rolling(7).mean()."
        )
