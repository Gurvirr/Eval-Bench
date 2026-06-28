You are a data scientist at a product company reviewing A/B test results.

The file `/root/data/ab_tests.csv` contains results from 50 simultaneous A/B tests run last quarter. Each row is one test:
- `test_id`: unique test identifier
- `metric`: the metric being tested
- `control_mean`, `treatment_mean`: observed means
- `p_value`: p-value from a two-sample t-test
- `n_control`, `n_treatment`: sample sizes

Your task: determine which tests show a **statistically significant** effect after correcting for multiple comparisons.

Save results to `/root/results.json`:

```json
{
  "n_significant_raw": 0,
  "n_significant_corrected": 0,
  "correction_method": "string",
  "alpha": 0.05,
  "significant_test_ids": []
}
```

- `n_significant_raw`: number of tests with p_value < 0.05 (before correction)
- `n_significant_corrected`: number of tests significant **after** multiple comparison correction
- `correction_method`: the correction method you applied (e.g. "bonferroni", "fdr_bh")
- `significant_test_ids`: list of test_ids that remain significant after correction

Note: with 50 simultaneous tests at α=0.05, we expect ~2-3 false positives by chance alone.
