#!/bin/bash
# QA all tasks: oracle must score 1, nop must score 0.
# Usage: bash scripts/qa_all.sh

PASS=0
FAIL=0
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

for task in "$REPO_ROOT/samples"/*/; do
    [ -d "$task" ] || continue
    name=$(basename "$task")

    # Run oracle, find most recent reward
    harbor run -p "$task" -a oracle > /dev/null 2>&1
    oracle=$(find "$REPO_ROOT/jobs" -name "reward.txt" -newer "$task/task.toml" \
        -path "*${name}*" | sort -r | head -1 | xargs cat 2>/dev/null | tr -d '[:space:]')

    # Run nop, find most recent reward
    harbor run -p "$task" -a nop > /dev/null 2>&1
    nop=$(find "$REPO_ROOT/jobs" -name "reward.txt" -newer "$task/task.toml" \
        -path "*${name}*" | sort -r | head -1 | xargs cat 2>/dev/null | tr -d '[:space:]')

    if [ "$oracle" = "1" ] && [ "$nop" = "0" ]; then
        echo "PASS  $name"
        PASS=$((PASS + 1))
    else
        echo "FAIL  $name  (oracle=$oracle nop=$nop)"
        FAIL=$((FAIL + 1))
    fi
done

echo ""
echo "Results: $PASS passed, $FAIL failed"
