"""
Verifier for multiple-comparisons task.

50 A/B tests. 2 have real effects (T003, T041).
Raw p<0.05: 4 tests (T003, T009, T029, T041) — includes 2 false positives
After Bonferroni: 2 tests (T003, T041) — the real effects only

The trap: agent reports n_significant_raw=4 as the answer,
or applies no correction and claims 4 significant results.

Correct: n_significant_corrected=2, significant_test_ids=["T003","T041"]
"""
import json
from pathlib import Path

RESULTS_FILE   = Path("/root/results.json")
CORRECT_IDS    = {"T003", "T041"}
EXPECTED_RAW   = 4


def load():
    assert RESULTS_FILE.exists(), f"Missing: {RESULTS_FILE}"
    return json.loads(RESULTS_FILE.read_text())


class TestMultipleComparisons:
    def test_output_exists(self):
        assert RESULTS_FILE.exists()

    def test_required_keys(self):
        d = load()
        for k in ["n_significant_raw","n_significant_corrected","correction_method","significant_test_ids"]:
            assert k in d, f"Missing key '{k}'"

    def test_raw_count_correct(self):
        """n_significant_raw must be 4 (the uncorrected count)."""
        d = load()
        assert int(d["n_significant_raw"]) == EXPECTED_RAW, \
            f"n_significant_raw={d['n_significant_raw']}, expected {EXPECTED_RAW}"

    def test_correction_applied(self):
        """
        n_significant_corrected must be 2, not 4.
        With 50 simultaneous tests at alpha=0.05, ~2-3 false positives
        are expected by chance. Without correction, T009 and T029 are
        false positives that should be rejected.
        """
        d = load()
        n = int(d["n_significant_corrected"])
        assert n <= 2, (
            f"n_significant_corrected={n}. After correcting for 50 simultaneous "
            f"tests (Bonferroni: alpha/50=0.001, or FDR), only 2 tests remain "
            f"significant. Without correction, ~2-3 false positives are expected."
        )

    def test_correct_tests_identified(self):
        """The significant tests must be T003 and T041 (the ones with real effects)."""
        d = load()
        reported = set(d["significant_test_ids"])
        assert reported == CORRECT_IDS, (
            f"significant_test_ids={sorted(reported)}, expected {sorted(CORRECT_IDS)}. "
            f"T009 and T029 are false positives that disappear after correction."
        )
