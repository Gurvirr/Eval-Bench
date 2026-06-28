#!/usr/bin/env python3
"""
Run all tasks against a model in parallel and print a live score table.
Usage: python scripts/run_all.py --model gemini/gemini-3.5-flash --trials 3
"""
import argparse
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

SAMPLES_DIR = Path(__file__).parent.parent / "samples"


def run_task(task_path: Path, model: str, trials: int, agent: str) -> tuple[str, int]:
    result = subprocess.run(
        ["harbor", "run", "-p", str(task_path), "-a", agent, "-m", model, "-n", str(trials)],
        capture_output=True, text=True
    )
    # Parse mean from output
    for line in result.stdout.splitlines():
        if "Mean:" in line:
            try:
                mean = float(line.split("Mean:")[1].strip().split()[0])
                return task_path.name, mean
            except (ValueError, IndexError):
                pass
    return task_path.name, -1.0


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="gemini/gemini-3.5-flash")
    parser.add_argument("--trials", type=int, default=3)
    parser.add_argument("--agent", default="terminus-2")
    parser.add_argument("--workers", type=int, default=4)
    args = parser.parse_args()

    tasks = sorted(p for p in SAMPLES_DIR.iterdir() if p.is_dir())
    if not tasks:
        print("No tasks found in samples/")
        sys.exit(1)

    print(f"Running {len(tasks)} tasks × {args.trials} trials with {args.model}\n")

    results = {}
    with ThreadPoolExecutor(max_workers=args.workers) as ex:
        futures = {ex.submit(run_task, t, args.model, args.trials, args.agent): t for t in tasks}
        for fut in as_completed(futures):
            name, mean = fut.result()
            results[name] = mean
            status = "✓" if mean > 0 else "✗"
            print(f"  {status} {name}: mean={mean:.3f}")

    print(f"\n{'Task':<35} {'Mean':>8}")
    print("-" * 45)
    for name in sorted(results):
        print(f"{name:<35} {results[name]:>8.3f}")
    overall = sum(results.values()) / len(results) if results else 0
    print(f"\nOverall mean: {overall:.3f}")


if __name__ == "__main__":
    main()
