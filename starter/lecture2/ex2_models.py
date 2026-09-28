"""Exercise 2: prior, Lecture 1 baselines, logistic regression, gradient boosting. Writes out/results.csv, importance.csv."""
import numpy as np, pandas as pd
from sklearn.pipeline import make_pipeline
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import StandardScaler, FunctionTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.inspection import permutation_importance
from common import *
df = pd.read_parquet(f"{OUT}/dataset.parquet")
# TODO: feature list; train/val/test frames from df.split
# TODO: bring in your Lecture 1 robust-z and rarity scores for the same rows (recompute with the SAME reference window)
# TODO: fit models on TRAIN only (preprocessing inside the Pipeline); score val and test
# TODO: results.csv columns: model,split,ap,tpr_at_0_1pct_fpr,p_at_k,recall_at_k (+ p_at_k_lo,p_at_k_hi on test)
# TODO: importance.csv (feature,importance) using scoring="average_precision" on VAL
# Save the val/test scores of your best model somewhere: Exercise 3 needs them.
raise SystemExit("TODO: implement Exercise 2")
