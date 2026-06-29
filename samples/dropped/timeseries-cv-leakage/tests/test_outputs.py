"""
Verifier for timeseries-cv-leakage task.

The trap: using KFold(shuffle=True) on time series data with a regime change
in year 3. Future data leaks into past training folds, underestimating true MAE.

KFold(shuffle=True) MAE: ~14.95 (too low — leaky)
TimeSeriesSplit MAE:      ~19.30 (correct)

We check:
1. cv_method contains "TimeSeriesSplit" (or "time series" / "tss")
2. cv_mean_mae > 17.0 (KFold gives ~14.95, TSS gives ~19.3)
"""
import json
from pathlib import Path

RESULTS_FILE = Path("/root/results.json")
TSS_MAE      = 19.2971
KFOLD_MAE    = 14.9522


def load():
    assert RESULTS_FILE.exists(), f"Missing: {RESULTS_FILE}"
    return json.loads(RESULTS_FILE.read_text())


class TestTimeseriesCV:
    def test_output_exists(self):
        assert RESULTS_FILE.exists()

    def test_required_keys(self):
        d = load()
        for k in ["cv_mean_mae", "cv_std_mae", "cv_method"]:
            assert k in d, f"Missing key '{k}'"

    def test_cv_method_is_timeseries(self):
        """
        Must use TimeSeriesSplit, not KFold.
        KFold(shuffle=True) leaks future data into past training folds
        when a distribution shift exists in the series.
        """
        d = load()
        method = str(d["cv_method"]).lower()
        assert "time" in method or "tss" in method or "series" in method, (
            f"cv_method='{d['cv_method']}'. For time series data, use "
            f"TimeSeriesSplit (sklearn.model_selection.TimeSeriesSplit) "
            f"instead of KFold. KFold shuffles temporal order and leaks "
            f"future data into training folds."
        )

    def test_mae_reflects_temporal_split(self):
        """
        cv_mean_mae must be > 17.0.
        KFold gives ~14.95 (underestimate due to leakage).
        TimeSeriesSplit gives ~19.3 (correct out-of-sample estimate).
        """
        d = load()
        mae = float(d["cv_mean_mae"])
        assert mae > 17.0, (
            f"cv_mean_mae={mae:.4f}. Expected > 17.0 with TimeSeriesSplit. "
            f"A value near {KFOLD_MAE:.2f} indicates KFold was used, "
            f"which leaks future data. Expected ~{TSS_MAE:.2f} with TimeSeriesSplit."
        )
