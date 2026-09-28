# CIS*6530 exercise pack: AI, ML and data mining for security analytics

```
data/lecture1/    eve.json  conn.log  auth.log  iocs.json  assets.csv  leases.csv
data/lecture2/    labels.csv  malware_features.parquet  reference_features.parquet
docs/             DATA_DICTIONARY.md
handouts/         lecture1_exercises.md   lecture2_exercises.md
starter/          lecture1/  lecture2/     (skeletons with TODOs; Makefiles)
tools/            check_lecture1.py  check_lecture2.py   (structure and sanity checks; they do not judge correctness)
```

## Setup
```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
# command-line tools: jq (>= 1.6) and GNU awk. macOS: brew install jq gawk
jq --version && gawk --version | head -1
```
All data is synthetic. Work in a git repository, keep raw data read-only, and write outputs to `out/`.
Start with `handouts/lecture1_exercises.md`. Lecture 2 builds on the feature table you make in Lecture 1, Exercise 5.

Run a check at any time:
```bash
python tools/check_lecture1.py --data data/lecture1 --out out
python tools/check_lecture2.py --data data/lecture2 --out out
```
