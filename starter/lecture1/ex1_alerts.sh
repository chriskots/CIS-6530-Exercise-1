#!/usr/bin/env bash
# Exercise 1: normalise Suricata alerts to UTC. Fill in the TODOs.
set -euo pipefail
DATA=${DATA:-../../data/lecture1}; OUT=${OUT:-../../out}; mkdir -p "$OUT"

# Look at the raw timestamps first:   jq -r '.timestamp' "$DATA/eve.json" | head
# TODO 1: a jq function `toepoch` that converts "2026-03-12T10:15:03.123456-0400" to UTC epoch seconds.
#         (Split off the offset with capture(); fromdateiso8601 wants "YYYY-MM-DDTHH:MM:SSZ".)
#         Reject impossible dates.
# TODO 2: emit  ts,bucket,src,dst,port,signature,severity  for event_type == "alert" (header line first).
# TODO 3: de-duplicate retransmitted events (hint: what field is unique per event?) and count rejected rows.
# TODO 4: bucket_counts.csv (bucket,n) and the busiest UTC hour.
echo "TODO: implement Exercise 1" >&2; exit 1
