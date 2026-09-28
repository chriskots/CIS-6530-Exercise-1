"""Exercise 6: robust z-score and rarity baselines. Reads out/features.parquet."""
import os, numpy as np, pandas as pd
OUT = os.environ.get("OUT", "../../out")
f = pd.read_parquet(f"{OUT}/features.parquet")
REF_END = pd.Timestamp("2026-02-22", tz="UTC")     # reference window = first 14 days ONLY
# TODO: log1p of >= 6 count-like features; median and MAD from rows before REF_END; floor the MAD
# TODO: rz_score = max upward robust z; rarity_score; ranks (1 = most anomalous)
# TODO: write ranked.csv (src_ip,hour,rz_score,rz_rank,rarity_score,rarity_rank) and top20_hosts.csv
raise SystemExit("TODO: implement Exercise 6")
