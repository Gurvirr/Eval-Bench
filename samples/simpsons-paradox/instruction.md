You are a data analyst reviewing a multi-site clinical trial of a new drug.

Data is stored across three hospital files under `/root/data/`:
- `hospital_a.csv` — columns: `pid`, `sev_group`, `arm`, `outcome`
- `hospital_b.csv` — columns: `patient_id`, `severity`, `treatment`, `recovered`
- `hospital_c.csv` — columns: `ID`, `Severity_Level`, `Treatment_Arm`, `Recovery_Status`

All three files record the same information: patient identifier, severity group (mild/moderate/severe), treatment arm (drug/control), and whether the patient recovered.

Note: `Recovery_Status` in hospital_c uses "Yes"/"No" instead of 1/0.

Combine all three datasets and analyze whether the drug improves recovery rates.

Save your findings to `/root/results.json`:

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
  "total_patients": 0,
  "drug_recommended": true or false
}
```

Round all rates to 4 decimal places.
