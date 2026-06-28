#!/usr/bin/env python3
"""
Aggregate pass@1 and pass@3 from harbor jobs/ output.
Usage:
  python scripts/aggregate_scores.py          # most recent 3 trials per task
  python scripts/aggregate_scores.py --n 5    # most recent 5 trials per task
  python scripts/aggregate_scores.py --all    # all trials ever
"""
import argparse
import re
from pathlib import Path

JOBS_DIR = Path(__file__).parent.parent / "jobs"
EXCLUDE  = {"restaurant-weekly-cost-control-a", ""}


def task_from_trial(name: str) -> str:
    return re.sub(r"__[A-Za-z0-9]+$", "", name)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--n",   type=int, default=3, help="Most recent N trials per task (default: 3)")
    parser.add_argument("--all", action="store_true",  help="Use all trials")
    args = parser.parse_args()

    # Collect all reward files sorted by modification time (newest last)
    entries: list[tuple[float, str, int]] = []  # (mtime, task, reward)
    for f in JOBS_DIR.rglob("reward.txt"):
        task = task_from_trial(f.parent.parent.name)
        if task in EXCLUDE:
            continue
        try:
            reward = int(f.read_text().strip())
            entries.append((f.stat().st_mtime, task, reward))
        except ValueError:
            pass

    # Group by task, take most recent N
    from collections import defaultdict
    by_task: dict[str, list[tuple[float, int]]] = defaultdict(list)
    for mtime, task, reward in entries:
        by_task[task].append((mtime, reward))

    n_label = "all" if args.all else f"recent {args.n}"
    print(f"Scores ({n_label} trials per task)\n")
    print(f"{'Task':<35} {'Trials':>6} {'pass@1':>8} {'pass@3':>8} {'mean':>8}")
    print("-" * 65)

    for task in sorted(by_task):
        trials_sorted = sorted(by_task[task], key=lambda x: x[0], reverse=True)
        if not args.all:
            trials_sorted = trials_sorted[:args.n]
        rewards = [r for _, r in trials_sorted]

        pass1 = rewards[0] if rewards else "?"
        pass3 = 1 if any(r == 1 for r in rewards) else (0 if len(rewards) >= 3 else "?")
        mean  = round(sum(rewards) / len(rewards), 2) if rewards else "?"
        print(f"{task:<35} {len(rewards):>6} {str(pass1):>8} {str(pass3):>8} {str(mean):>8}")


if __name__ == "__main__":
    main()
