"""Exercise 5: host-hour feature table. Writes out/features.parquet and out/audit.csv."""
import os, json, math
import numpy as np, pandas as pd
DATA = os.environ.get("DATA", "../../data/lecture1"); OUT = os.environ.get("OUT", "../../out"); os.makedirs(OUT, exist_ok=True)
audit = []
def A(check, finding, action): audit.append(dict(check=check, finding=finding, action=action))

# 1. load eve.json into a DataFrame (json.loads per line -> pd.json_normalize)
# 2. parse timestamps to UTC with errors="coerce"; count the bad ones -> A("Unparseable timestamps", ...); drop them
# 3. drop duplicate events (which column identifies an event?) -> A("Duplicate events", ...)
# 4. alerts only: hour = ts.floor("h"); groupby(["src_ip","hour"]) named aggregation for the required columns
# 5. offhours (America/Toronto), sig_rarity (PRIOR days only)
# 6. optional features: DNS entropy, conn.log features, ioc_hit, merge_asof leases -> assets (watch assets.csv!)
# 7. assert the key is unique; set dtypes; save parquet; write audit.csv (check,finding,action)
raise SystemExit("TODO: implement Exercise 5")
