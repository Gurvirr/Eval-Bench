# Scripts

## Workflow

### 1. After changing any task — verify it's not broken
```bash
bash scripts/qa_all.sh
```
Oracle should score 1, nop should score 0 for every task.

### 2. Run all tasks against the model
```powershell
python scripts/run_all.py --model gemini/gemini-3.5-flash --trials 3
```
Takes ~15-20 min. Runs all 7 tasks in parallel.

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
