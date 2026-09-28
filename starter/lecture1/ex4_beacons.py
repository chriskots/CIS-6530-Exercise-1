"""Exercise 4, step 2: rank beacon candidates. Reads out/deltas.tsv, writes out/beacons.csv (top 10)."""
import os, pandas as pd, numpy as np
OUT = os.environ.get("OUT", "../../out")
d = pd.read_csv(f"{OUT}/deltas.tsv", sep="\t")
# TODO: per pair: n, mean_gap, std -> cv, size_cv; hosts per destination; keep n >= 50
# TODO: rank-average score (low cv, low size_cv, few hosts); top 10 -> beacons.csv with
#       columns pair,n,mean_gap,cv,size_cv,hosts,score
raise SystemExit("TODO: implement Exercise 4")
