#!/usr/bin/env python3
"""
Classify failure modes from trajectory.json files in failed runs.
Usage: python scripts/classify_failures.py
"""
import json
import re
from pathlib import Path

JOBS_DIR = Path(__file__).parent.parent / "jobs"

FAILURE_PATTERNS = [
    ("took_the_trap",    ["fit_transform", "combined", "all data", "full dataset",
                          "rolling(7)", ".rolling(", "without shift",
                          "overall rate", "overall recovery", "recommend.*true",
                          "merge.*tags.*sum", "join.*then.*sum"]),
    ("wrong_metric",     ["accuracy", "weighted", "f1_weighted", "macro.*wrong",
                          "recommend.*deploy.*true", "97.*accur"]),
    ("format_error",     ["KeyError", "key not found", "missing key", "json",
                          "results.json", "no such file", "FileNotFound"]),
    ("arithmetic_slip",  ["rounding", "precision", "off by", "mismatch", "expected.*got"]),
    ("reasoning_error",  ["misread", "misunderstand", "incorrect", "wrong assumption"]),
]


def classify(text: str) -> str:
    text_lower = text.lower()
    for label, patterns in FAILURE_PATTERNS:
        if any(p.lower() in text_lower for p in patterns):
            return label
    return "unknown"


def extract_text(trajectory: dict) -> str:
    texts = []
    for step in trajectory.get("steps", []):
        content = step.get("message", "") or step.get("content", "")
        if isinstance(content, list):
            for c in content:
                if isinstance(c, dict):
                    texts.append(c.get("text", ""))
        elif content:
            texts.append(str(content))
    return " ".join(texts)


print(f"{'Task':<35} {'Reward':>7} {'Failure Type':<25} {'Excerpt'}")
print("-" * 100)

for reward_file in sorted(JOBS_DIR.rglob("reward.txt")):
    reward = reward_file.read_text().strip()
    if reward != "0":
        continue

    trial_dir = reward_file.parent.parent
    task = re.sub(r"__[A-Za-z0-9]+$", "", trial_dir.name)
    if task in ("", "restaurant-weekly-cost-control-a"):
        continue

    traj_file = trial_dir / "agent" / "trajectory.json"
    if not traj_file.exists():
        print(f"{task:<35} {'0':>7} {'no_trajectory':<25}")
        continue

    try:
        traj = json.loads(traj_file.read_text())
        text = extract_text(traj)
        failure_type = classify(text)

        # Get a short excerpt from the last assistant message
        excerpt = ""
        for step in reversed(traj.get("steps", [])):
            msg = step.get("message", "")
            if msg and step.get("source") == "agent":
                excerpt = msg[:120].replace("\n", " ")
                break

        print(f"{task:<35} {'0':>7} {failure_type:<25} {excerpt}")
    except Exception as e:
        print(f"{task:<35} {'0':>7} {'parse_error':<25} {e}")
