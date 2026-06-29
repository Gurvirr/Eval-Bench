You are a data analyst at a healthcare company reviewing a clinical trial.

Files under `/root/data/`:
- `trial.csv` — trial results: `patient_id`, `treatment` (drug/control), `recovered` (1/0)
- `patient_metadata.csv` — patient info: `patient_id`, `severity_group`, `age`, `hospital_id`

Analyze whether the drug improves recovery rates and save to `/root/results.json`:

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

Round all rates to 4 decimal places.
