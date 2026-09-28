#!/usr/bin/env python3
"""Structure and sanity checks for Lecture 2 outputs. It does NOT judge correctness.
Usage: python tools/check_lecture2.py --data data/lecture2 --out out"""
import argparse, os, sys
import pandas as pd, numpy as np
ap = argparse.ArgumentParser(); ap.add_argument("--data", default="data/lecture2"); ap.add_argument("--out", default="out"); a = ap.parse_args()
ok_all = True
def report(name, ok, msg=""):
    global ok_all; ok_all &= bool(ok); print(("PASS  " if ok else "FAIL  ") + name + (f": {msg}" if msg else ""))
def exists(p): return os.path.exists(os.path.join(a.out, p))

print("== Exercise 1 ==")
if exists("dataset.parquet"):
    d = pd.read_parquet(f"{a.out}/dataset.parquet"); need = ["src_ip", "hour", "label", "label_source", "label_ts", "split"]
    miss = [c for c in need if c not in d.columns]; report("required columns", not miss, f"missing {miss}" if miss else "")
    if not miss:
        report("(src_ip, hour) unique", not d.duplicated(["src_ip", "hour"]).any()); report("label is 0/1", set(d.label.unique()) <= {0, 1})
        report("split values", set(d.split.unique()) <= {"train", "val", "test", "gap"}, str(sorted(d.split.unique())))
        h = d.groupby("split").hour.agg(["min", "max"])
        if {"train", "val", "test"} <= set(h.index):
            report("splits are in time order (train < val < test)", h.loc["train", "max"] < h.loc["val", "min"] and h.loc["val", "max"] < h.loc["test", "min"])
            report("a gap separates train and val", (h.loc["val", "min"] - h.loc["train", "max"]) >= pd.Timedelta("12h"), str(h.loc["val", "min"] - h.loc["train", "max"]))
        print("      positives per split:", d.groupby("split").label.sum().to_dict(), " prevalence:", round(d.label.mean(), 4))
        report("test positives >= 20 (or say why not)", d[d.split == "test"].label.sum() >= 20)
else: report("dataset.parquet exists", False)
report("leakage_screen.csv exists", exists("leakage_screen.csv")); report("SPLITS.md exists", exists("SPLITS.md"))

print("== Exercise 2 ==")
if exists("results.csv"):
    r = pd.read_csv(f"{a.out}/results.csv"); need = ["model", "split", "ap", "tpr_at_0_1pct_fpr", "p_at_k", "recall_at_k"]; miss = [c for c in need if c not in r.columns]
    report("results.csv columns", not miss, f"missing {miss}" if miss else "")
    if not miss:
        ms = set(r.model.str.lower()); report("prior, both baselines, logistic and boosting all present", len(ms) >= 5, str(sorted(ms)))
        report("val and test rows for every model", (r.groupby("model").split.nunique() == 2).all())
        report("metrics in [0, 1]", r[["ap", "tpr_at_0_1pct_fpr", "p_at_k", "recall_at_k"]].apply(lambda s: s.between(0, 1)).all().all())
        report("test rows carry a bootstrap interval", {"p_at_k_lo", "p_at_k_hi"} <= set(r.columns))
        best = r[r.split == "test"].ap.max(); report("suspicion check: test AP above 0.95 is a bug until proven otherwise", best < 0.95, f"best test AP {best:.3f}")
else: report("results.csv exists", False)
report("importance.csv exists", exists("importance.csv"))

print("== Exercise 3 ==")
if exists("queue.csv"):
    q = pd.read_csv(f"{a.out}/queue.csv"); need = ["day", "rank", "src_ip", "hour", "score", "label", "explore"]; miss = [c for c in need if c not in q.columns]
    report("queue.csv columns", not miss, f"missing {miss}" if miss else "")
    if not miss:
        per = q.groupby("day").size(); report("the same number of rows every day (the budget K)", per.nunique() == 1, f"K={per.iloc[0]}" if per.nunique() == 1 else str(per.unique()))
        report("an exploration slice exists", q.explore.astype(str).str.lower().isin(["true", "1"]).any())
else: report("queue.csv exists", False)
for f in ("gain.png", "calibration.png", "TRIAGE.md"): report(f"{f} exists", exists(f))

print("== Exercise 4 ==")
if exists("malware_results.csv"):
    m = pd.read_csv(f"{a.out}/malware_results.csv"); report("three evaluations reported (random, grouped, time)", len(m) >= 3 and {"split", "ap", "tpr_at_0_1pct_fpr", "tpr_at_1pct_fpr"} <= set(m.columns))
else: report("malware_results.csv exists", False)
for f in ("malware_drift.png", "ember_report.md"): report(f"{f} exists", exists(f))

print("== Exercise 5 ==")
report("model card exists (model_card.md or model_card.pdf)", exists("model_card.md") or exists("model_card.pdf"))
print("\nAll structural checks passed." if ok_all else "\nSome checks failed: read the FAIL lines above.")
sys.exit(0 if ok_all else 1)
