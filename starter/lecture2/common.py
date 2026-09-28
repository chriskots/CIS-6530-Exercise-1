"""Shared settings and helpers for Lecture 2. Read it, then extend it."""
import os, numpy as np, pandas as pd
from sklearn.metrics import average_precision_score, roc_curve
DATA = os.environ.get("DATA", "../../data/lecture2"); OUT = os.environ.get("OUT", "../../out"); os.makedirs(OUT, exist_ok=True)
T1 = pd.Timestamp("2026-03-01", tz="UTC"); T2 = pd.Timestamp("2026-03-08", tz="UTC"); GAP = pd.Timedelta("1D")
K = 15   # analyst budget: host-hours reviewed per day

def add_split(df):
    """train: hour < T1-GAP; val: T1 <= hour < T2-GAP; test: hour >= T2; everything else 'gap'."""
    s = np.full(len(df), "gap", dtype=object); h = df["hour"]
    s[h < T1 - GAP] = "train"; s[(h >= T1) & (h < T2 - GAP)] = "val"; s[h >= T2] = "test"
    return df.assign(split=s)

def tpr_at_fpr(y, score, fpr_target):
    fpr, tpr, _ = roc_curve(y, score); return float(np.interp(fpr_target, fpr, tpr))

def p_at_k(df, k=K, score="score", label="label"):
    """Mean precision of the top-k rows per UTC day. Expects columns: hour, score, label."""
    d = df.assign(day=df["hour"].dt.floor("D"))
    return d.sort_values(score, ascending=False).groupby("day").head(k)[label].mean()

# TODO (Exercise 2): recall_at_k(...)
# TODO (Exercise 2): a bootstrap that resamples HOSTS (src_ip), not rows, returning a 95% interval.
#   Hint: group row indices by src_ip once, then resample the list of hosts and concatenate their rows.
