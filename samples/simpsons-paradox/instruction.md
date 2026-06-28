You are a data analyst at a healthcare company reviewing a clinical trial.

The file `/root/data/trial.csv` contains results from a randomized trial of a new drug:
- `patient_id` — unique patient identifier
- `severity` — patient severity group (mild, moderate, or severe)
- `treatment` — "drug" or "control"
- `recovered` — 1 if recovered, 0 if not
- `hospital_id` — hospital where the patient was treated

Analyze the data and save your findings to `/root/results.json`:

```json
{
  "overall_drug_recovery_rate": 0.XXXX,
  "overall_control_recovery_rate": 0.XXXX,
  "mild_drug_recovery_rate": 0.XXXX,
  "mild_control_recovery_rate": 0.XXXX,
  "moderate_drug_recovery_rate": 0.XXXX,
  "moderate_control_recovery_rate": 0.XXXX,
  "severe_drug_recovery_rate": 0.XXXX,
  "severe_control_recovery_rate": 0.XXXX,
  "drug_recommended": true or false
}
```

`drug_recommended` should be `true` if the evidence supports recommending the drug, `false` otherwise.

Round all rates to 4 decimal places.
