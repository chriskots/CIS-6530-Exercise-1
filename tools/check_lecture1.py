#!/usr/bin/env python3
"""Structure and sanity checks for Lecture 1 outputs. It does NOT judge correctness.
Usage: python tools/check_lecture1.py --data data/lecture1 --out out"""
import argparse, json, os, re, sys
import pandas as pd, numpy as np
ap = argparse.ArgumentParser(); ap.add_argument("--data", default="data/lecture1"); ap.add_argument("--out", default="out"); ap.add_argument("--fast", action="store_true")
a = ap.parse_args()
ok_all = True
def report(name, ok, msg=""):
    global ok_all; ok_all &= bool(ok); print(("PASS  " if ok else "FAIL  ") + name + (f": {msg}" if msg else ""))
def exists(p): return os.path.exists(os.path.join(a.out, p))

print("== Exercise 1 ==")
if exists("alerts.csv"):
    d = pd.read_csv(f"{a.out}/alerts.csv")
    need = ["ts", "bucket", "src", "dst", "port", "signature", "severity"]
    report("columns start with ts,bucket,src,dst,port,signature,severity", list(d.columns[:7]) == need, str(list(d.columns[:7])))
    if list(d.columns[:7]) == need:
        report("ts are integers in the data window", d.ts.notna().all() and d.ts.between(1770508800 - 86400, 1773532800 + 86400).all())
        report("bucket = floor(ts/300)*300", (d.bucket == (d.ts // 300) * 300).all())
        # canary events: each must appear with exactly this UTC epoch. Catches wrong offsets and DST mistakes.
        canaries = [(1772951396, "10.20.2.20", "10.20.2.40", 445, "LAB Large Outbound Transfer", "before the DST jump"),
                    (1772956871, "10.20.5.85", "88.133.220.169", 443, "LAB Outdated TLS Version", "after the DST jump"),
                    (1773327596, "10.20.5.86", "14.151.180.42", 80, "LAB Suspicious User-Agent", "mid March"),
                    (1770799992, "19.4.254.203", "10.20.2.80", 80, "LAB Web Scanner Probe", "February")]
        for ts, s, dst, p, sig, why in canaries:
            hit = ((d.src == s) & (d.dst == dst) & (d.port == p) & (d.signature == sig) & (d.ts == ts)).any()
            report(f"canary event ({why})", hit, "" if hit else "expected epoch not found: recheck the offset handling")
else: report("alerts.csv exists", False)
report("bucket_counts.csv exists", exists("bucket_counts.csv"))

print("== Exercise 2 ==")
if exists("enriched.ndjson"):
    n_in = sum(1 for _ in open(f"{a.data}/eve.json")); n = 0; keys_ok = True; bad_types = 0
    with open(f"{a.out}/enriched.ndjson") as fh:
        for i, l in enumerate(fh):
            n += 1
            if i < 2000:
                o = json.loads(l)
                if "alert.severity" not in o and o.get("event_type") == "alert": keys_ok = False
                if not isinstance(o.get("ioc_hit"), bool) or not isinstance(o.get("src_private"), bool): bad_types += 1
    report("one output line per input event", n == n_in, f"{n} vs {n_in}")
    report("keys are flattened with dots", keys_ok); report("ioc_hit and src_private are booleans", bad_types == 0)
else: report("enriched.ndjson exists", False)
report("ex2_memory.txt exists", exists("ex2_memory.txt"))

print("== Exercise 3 ==")
if exists("ssh_report.tsv"):
    s = pd.read_csv(f"{a.out}/ssh_report.tsv", sep="\t")
    need = ["src_ip", "failures", "distinct_users", "first_fail", "last_fail", "success_after_fail", "likely_compromise"]
    report("columns", list(s.columns) == need, str(list(s.columns)))
    if list(s.columns) == need:
        report("every row has >= 10 failures and src_ip is unique", (s.failures >= 10).all() and s.src_ip.is_unique)
        # independent recount of failures per address
        c, u = {}, {}
        for l in open(f"{a.data}/auth.log"):
            if "Failed password" in l:
                m = re.search(r"Failed password for (?:invalid user )?(\S+) from (\S+) port", l)
                if m: c[m.group(2)] = c.get(m.group(2), 0) + 1; u.setdefault(m.group(2), set()).add(m.group(1))
        exp = {k for k, v in c.items() if v >= 10}
        report("set of sources with >= 10 failures matches an independent recount", set(s.src_ip) == exp, f"yours {len(s)}, recount {len(exp)}")
        mm = s[[c.get(i, -1) != f or len(u.get(i, ())) != d for i, f, d in zip(s.src_ip, s.failures, s.distinct_users)]]
        report("failures and distinct_users match the recount", len(mm) == 0, f"{len(mm)} rows differ")
        report("success_after_fail and likely_compromise are yes/no", s.success_after_fail.isin(["yes", "no"]).all() and s.likely_compromise.isin(["yes", "no"]).all())
else: report("ssh_report.tsv exists", False)

print("== Exercise 4 ==")
if exists("deltas.tsv"):
    d = pd.read_csv(f"{a.out}/deltas.tsv", sep="\t", nrows=1000); report("deltas.tsv columns", list(d.columns) == ["pair", "delta_s", "orig_bytes"], str(list(d.columns)))
    report("deltas are non-negative", (d.delta_s >= 0).all())
else: report("deltas.tsv exists", False)
if exists("beacons.csv"):
    b = pd.read_csv(f"{a.out}/beacons.csv"); report("beacons.csv has 10 rows and the required columns", len(b) == 10 and {"pair", "n", "mean_gap", "cv", "size_cv", "hosts", "score"} <= set(b.columns))
    report("every candidate has n >= 50", (b.n >= 50).all())
else: report("beacons.csv exists", False)

print("== Exercise 5 ==")
if exists("features.parquet"):
    f = pd.read_parquet(f"{a.out}/features.parquet")
    core = ["src_ip", "hour", "n_alerts", "n_sigs", "n_dst", "n_ports", "sev_min", "sev_mean", "offhours", "sig_rarity"]
    miss = [c for c in core if c not in f.columns]; report("core columns present", not miss, f"missing {miss}" if miss else "")
    if not miss:
        report("hour is timezone-aware UTC, floored to the hour", str(f.hour.dt.tz) == "UTC" and (f.hour == f.hour.dt.floor("h")).all(), str(f.hour.dtype))
        report("(src_ip, hour) is unique", not f.duplicated(["src_ip", "hour"]).any())
        report("no missing values in core columns", not f[core].isna().any().any())
        report("offhours is 0/1", set(f.offhours.unique()) <= {0, 1})
        report("at least four optional feature columns", len([c for c in f.columns if c not in core]) >= 4, f"{len([c for c in f.columns if c not in core])} extra")
        report("severity in 1..3 and n_alerts >= 1", f.sev_min.between(1, 3).all() and (f.n_alerts >= 1).all())
        if not a.fast:
            n_ok = 0; seen = set(); pat = re.compile(r'^(\d{4})-(\d{2})-(\d{2})T(\d{2}):(\d{2}):(\d{2})\.\d+([+-])(\d{2})(\d{2})$')
            import datetime as dt
            for l in open(f"{a.data}/eve.json"):
                o = json.loads(l)
                if o.get("event_type") != "alert": continue
                m = pat.match(str(o.get("timestamp")))
                if not m: continue
                try: dt.datetime(*[int(x) for x in m.groups()[:6]])
                except ValueError: continue
                if o["flow_id"] in seen: continue
                seen.add(o["flow_id"]); n_ok += 1
            report("sum(n_alerts) equals the number of unique alerts with parseable timestamps", int(f.n_alerts.sum()) == n_ok, f"yours {int(f.n_alerts.sum())}, recount {n_ok} (only a mismatch if you documented a different rule)")
else: report("features.parquet exists", False)
if exists("audit.csv"):
    au = pd.read_csv(f"{a.out}/audit.csv"); report("audit.csv columns check,finding,action", list(au.columns) == ["check", "finding", "action"] and len(au) >= 6, f"{len(au)} rows")
else: report("audit.csv exists", False)

print("== Exercise 6 ==")
if exists("ranked.csv"):
    r = pd.read_csv(f"{a.out}/ranked.csv"); need = ["src_ip", "hour", "rz_score", "rz_rank", "rarity_score", "rarity_rank"]
    report("ranked.csv columns", list(r.columns[:6]) == need, str(list(r.columns[:6])))
    report("ranks start at 1", r.rz_rank.min() == 1 and r.rarity_rank.min() == 1)
else: report("ranked.csv exists", False)
report("top20_hosts.csv exists", exists("top20_hosts.csv")); report("ANALYST_NOTE.md exists", exists("ANALYST_NOTE.md"))
print("\nAll structural checks passed." if ok_all else "\nSome checks failed: read the FAIL lines above.")
sys.exit(0 if ok_all else 1)
