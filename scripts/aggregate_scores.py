#!/usr/bin/env python3
"""
Aggregate pass@1 and pass@3 from harbor jobs/ output.
Usage: python scripts/aggregate_scores.py
"""
import json
import re
from pathlib import Path
from collections import defaultdict

JOBS_DIR = Path(__file__).parent.parent / "jobs"

# Map trial folder name prefix to task name
def task_from_trial(trial_name: str) -> str:
    # e.g. "leakage-imputation__abc123" -> "leakage-imputation"
    return re.sub(r"__[A-Za-z0-9]+$", "", trial_name)

scores: dict[str, list[int]] = defaultdict(list)

for reward_file in sorted(JOBS_DIR.rglob("reward.txt")):
    trial_dir = reward_file.parent.parent
    task = task_from_trial(trial_dir.name)
    if not task or task in ("", "restaurant-weekly-cost-control-a"):
        continue
    try:
        reward = int(reward_file.read_text().strip())
        scores[task].append(reward)
    except ValueError:
        continue

print(f"{'Task':<35} {'Trials':>6} {'pass@1':>8} {'pass@3':>8} {'mean':>8}")
print("-" * 70)

for task in sorted(scores):
    trials = scores[task]
    n = len(trials)
    pass1 = trials[0] if n >= 1 else "?"
    pass3 = 1 if any(t == 1 for t in trials[:3]) else 0 if n >= 3 else "?"
    mean = round(sum(trials) / n, 2) if n > 0 else "?"
    print(f"{task:<35} {n:>6} {str(pass1):>8} {str(pass3):>8} {str(mean):>8}")
