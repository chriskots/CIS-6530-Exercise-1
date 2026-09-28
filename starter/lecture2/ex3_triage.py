"""Exercise 3: calibrated daily queue, gain curve, calibration plot."""
import numpy as np, pandas as pd, matplotlib
matplotlib.use("Agg"); import matplotlib.pyplot as plt
from sklearn.isotonic import IsotonicRegression
from sklearn.calibration import calibration_curve
from common import *
# TODO 1: load your saved val/test scores; fit the calibrator on VAL only; apply to TEST
# TODO 2: per test day: top K-n_explore by score plus n_explore random rows outside the top (explore=True) -> queue.csv
#         columns: day,rank,src_ip,hour,score,label,explore
# TODO 3: gain.png and calibration.png (quantile bins)
# TODO 4: numbers for TRIAGE.md: precision@K, recall@K (with host-bootstrap intervals), lift, rows to reach 80% recall
raise SystemExit("TODO: implement Exercise 3")
