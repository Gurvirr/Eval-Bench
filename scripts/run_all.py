#!/usr/bin/env python3
"""
Run all tasks against a model in parallel and print a score table.
Usage: python scripts/run_all.py --model gemini/gemini-3.5-flash --trials 3
"""
import argparse
import json
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

SAMPLES_DIR = Path(__file__).parent.parent / "samples"
JOBS_DIR    = Path(__file__).parent.parent / "jobs"


def latest_reward(task_name: str, after_ts: float) -> float | None:
    """Find the most recent reward for a task run after a given timestamp."""
    for reward_file in sorted(JOBS_DIR.rglob("reward.txt"), key=lambda p: p.stat().st_mtime, reverse=True):
        if reward_file.stat().st_mtime < after_ts:
            continue
        trial_dir = reward_file.parent.parent
        if trial_dir.name.startswith(task_name):
            try:
                return float(reward_file.read_text().strip())
            except ValueError:
                pass
    return None


def run_task(task_path: Path, model: str, trials: int, agent: str) -> tuple[str, list[float]]:
    import time
    start = time.time()
    subprocess.run(
        ["harbor", "run", "-p", str(task_path), "-a", agent, "-m", model, "-n", str(trials)],
        capture_output=True, text=True
    )
    # Read reward files written after we started
    rewards = []
    for reward_file in sorted(JOBS_DIR.rglob("reward.txt"), key=lambda p: p.stat().st_mtime):
        if reward_file.stat().st_mtime < start:
            continue
        trial_dir = reward_file.parent.parent
        if trial_dir.name.startswith(task_path.name):
            try:
                rewards.append(float(reward_file.read_text().strip()))
            except ValueError:
                pass
    return task_path.name, rewards


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model",   default="gemini/gemini-3.5-flash")
    parser.add_argument("--trials",  type=int, default=3)
    parser.add_argument("--agent",   default="terminus-2")
    parser.add_argument("--workers", type=int, default=4)
    args = parser.parse_args()

    tasks = sorted(p for p in SAMPLES_DIR.iterdir() if p.is_dir())
    if not tasks:
        print("No tasks found in samples/"); sys.exit(1)

    print(f"Running {len(tasks)} tasks × {args.trials} trials | model={args.model} | workers={args.workers}\n")

    results: dict[str, list[float]] = {}
    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        futures = {ex.submit(run_task, t, args.model, args.trials, args.agent): t for t in tasks}
        for fut in as_completed(futures):
            name, rewards = fut.result()
            results[name] = rewards
            mean = sum(rewards) / len(rewards) if rewards else float("nan")
            mark = "✓" if mean >= 0.5 else "✗"
            print(f"  {mark} {name}: {rewards} mean={mean:.2f}")

    print(f"\n{'Task':<35} {'Trials':>6} {'mean':>8} {'pass@3':>8}")
    print("-" * 60)
    for name in sorted(results):
        r = results[name]
        mean = sum(r) / len(r) if r else float("nan")
        pass3 = 1 if any(x == 1 for x in r[:3]) else (0 if len(r) >= 3 else "?")
        print(f"{name:<35} {len(r):>6} {mean:>8.2f} {str(pass3):>8}")


if __name__ == "__main__":
    main()
