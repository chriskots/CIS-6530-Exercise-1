#!/usr/bin/env bash
# Exercise 2: flatten every event, add ioc_hit and src_private, stream with -n / inputs.
set -euo pipefail
DATA=${DATA:-../../data/lecture1}; OUT=${OUT:-../../out}; mkdir -p "$OUT"
# TODO: jq -nc --slurpfile ioc "$DATA/iocs.json" '... inputs ...' "$DATA/eve.json" > "$OUT/enriched.ndjson"
#       Wrap with /usr/bin/time -v (Linux) or /usr/bin/time -l (macOS) and save peak memory to $OUT/ex2_memory.txt
echo "TODO: implement Exercise 2" >&2; exit 1
