#!/bin/bash
# QA all tasks: run oracle + nop for each sample, print pass/fail table.
# Usage: bash scripts/qa_all.sh

set -e

PASS=0
FAIL=0

for task in samples/*/; do
    [ -d "$task" ] || continue
    name=$(basename "$task")

    oracle_reward=$(harbor run -p "$task" -a oracle 2>/dev/null | tail -1)
    nop_reward=$(harbor run -p "$task" -a nop 2>/dev/null | tail -1)

    if [ "$oracle_reward" = "1" ] && [ "$nop_reward" = "0" ]; then
        echo "PASS  $name"
        PASS=$((PASS + 1))
    else
        echo "FAIL  $name  (oracle=$oracle_reward nop=$nop_reward)"
        FAIL=$((FAIL + 1))
    fi
done

echo ""
echo "Results: $PASS passed, $FAIL failed"
