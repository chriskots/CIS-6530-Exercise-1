"""Exercise 1: labelled dataset, splits, leakage screen. Writes out/dataset.parquet, leakage_screen.csv."""
import numpy as np, pandas as pd
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import StratifiedGroupKFold
from common import *
features_path = os.path.join(DATA, "reference_features.parquet")     # TODO: switch to YOUR features.parquet if you have it
f = pd.read_parquet(features_path)
labels = pd.read_csv(f"{DATA}/labels.csv", parse_dates=["hour", "label_ts"])
# TODO 1: make labels' hour dtype match f["hour"] (timezone-aware UTC), then merge with validate="1:1"
# TODO 2: label = label.fillna(0).astype(int); df = add_split(df); print rows / positives / prevalence / positives by label_source
# TODO 3: single-feature AUC screen on TRAIN rows -> leakage_screen.csv (feature,auc,flagged)
# TODO 4: share of positives with ioc_hit == 1 by label_source
# TODO 5: StratifiedGroupKFold(5) on src_ip -> a `group_fold` column; positives per fold
# Finally: df.to_parquet(f"{OUT}/dataset.parquet")   (columns must include label, label_source, label_ts, split)
raise SystemExit("TODO: implement Exercise 1")
