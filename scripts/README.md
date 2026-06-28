# Scripts

## Workflow

### 1. After changing any task — verify it's not broken
```bash
bash scripts/qa_all.sh
```
Oracle should score 1, nop should score 0 for every task.

### 2. Run all tasks against the model
```powershell
.\scripts\run_model.bat
```
Takes ~35 min (sequential, 3 trials per task via `-k 3`). Results go into `jobs/`.

### 3. Check scores
```powershell
python scripts/aggregate_scores.py
```
Shows pass@1, pass@3, mean for most recent 3 trials per task.

### 4. Understand failures
```powershell
python scripts/classify_failures.py
```
For every failed run, shows what the model did wrong.
