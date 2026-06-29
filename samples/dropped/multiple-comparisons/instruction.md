You are a data scientist reviewing last quarter's experiment results.

The directory `/root/data/tests/` contains 50 CSV files, one per A/B test (`T001.csv` through `T050.csv`). Each file has columns:
- `group` — "control" or "treatment"  
- `value` — the metric value for that user

Your task: identify which experiments show a statistically significant effect.

Save results to `/root/results.json`:

```json
{
  "n_significant_raw": 0,
  "n_significant_corrected": 0,
  "correction_method": "string",
  "significant_test_ids": []
}
```

- `n_significant_raw`: tests with p_value < 0.05 before any correction
- `n_significant_corrected`: tests significant after correcting for multiple comparisons
- `correction_method`: the method applied
- `significant_test_ids`: test IDs remaining significant after correction (e.g. ["T003", "T041"])
