# eval-bench

A mini evaluation benchmark of data-science tasks targeting known failure modes in frontier LLM agents.

Each task is a [Harbor](https://harborframework.com)-format problem isolating a specific, well-documented pitfall in real-world data science: data leakage, look-ahead bias in time-series, aggregation paradoxes, metric definition errors, and messy multi-modal I/O. The benchmark targets < 30% pass@3 against `gemini-3.5-flash`.

## Repo Structure

```
samples/        # Harbor-format task packages (one directory per task)
report/         # Write-up: distribution rationale, difficulty profile, scale plan
scripts/        # Automation: QA runner, score aggregator, failure classifier
logs/           # harbor run output — gitignored, local only
```

## Quickstart

Requires Docker and Harbor installed.

```bash
pip install harbor-ai

# Validate a single task
harbor run -p samples/<task-name> -a oracle      # expect reward 1
harbor run -p samples/<task-name> -a nop         # expect reward 0

# Run against the model under test (≥3 trials)
harbor run -p samples/<task-name> -a terminus-2 -m gemini/gemini-3.5-flash

# QA all tasks at once
bash scripts/qa_all.sh
```

## Task Index

| Task | Failure Mode | pass@1 | pass@3 |
|------|-------------|--------|--------|
| TBD  | TBD         | TBD    | TBD    |
