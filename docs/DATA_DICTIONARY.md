# Data dictionary

All data is **synthetic**. Hosts, users, domains and incidents are invented, and public IPv4 addresses are random and
carry no meaning. Real logs are messier still. The pack covers **8 Feb 2026 00:00 UTC to 15 Mar 2026 00:00 UTC** (35 days)
for a fictional organisation whose internal address space is `10.20.0.0/16`.

## Lecture 1: `data/lecture1/`

| File | Format | Notes |
|---|---|---|
| `eve.json` | NDJSON, one Suricata-style event per line | `event_type` is `alert`, `dns`, `http`, `tls` or `flow`. Alerts carry `alert.signature`, `alert.severity`, and sometimes `http`, `tls` or `dns` sub-objects. |
| `conn.log` | Zeek TSV, header lines start with `#` | 13 columns: `ts uid id.orig_h id.orig_p id.resp_h id.resp_p proto service duration orig_bytes resp_bytes conn_state history`. `ts` is epoch seconds (UTC). Unset values are `-`. |
| `auth.log` | syslog text from the bastion host (`bastion01`) | Local time, **no year**. Lines: `Failed password`, `Accepted password`, `Accepted publickey`, `Disconnected`. |
| `iocs.json` | one JSON array of IP strings | Threat-intel list. It is **imperfect**: many entries are noise, and some real attacker addresses are missing. |
| `assets.csv` | CSV | `host, owner, criticality, role`. Not every host is present, and it is not guaranteed to be clean. |
| `leases.csv` | CSV | `ip, host, start` (UTC). DHCP lease starts and static reservations. A row means *host held this IP from `start` until a later row for that host or IP replaces it*. |

**Time.** The Suricata sensor writes **local time (America/Toronto) with a numeric offset**, e.g. `2026-03-12T10:15:03.123456-0400`.
Daylight-saving time began on **8 March 2026 at 02:00 local**. `conn.log` is UTC epoch seconds. `auth.log` is local time without a year.

**Known quirks** (finding and handling these is part of the exercise): bad timestamps, duplicated events, a sensor outage,
sparse fields, addresses that change owner, and an `assets.csv` you should not trust blindly.

## Lecture 2: `data/lecture2/`

| File | Notes |
|---|---|
| `labels.csv` | `src_ip, hour (UTC), label (0/1), label_source, label_ts`. **Sparse**: it covers only host-hours someone reviewed or a process flagged. `label_source` is `analyst_disposition`, `incident_ticket` or `ioc_match`. `label_ts` is when the label became known. Unlisted host-hours are *unlabelled*, which you will treat as benign (say so in your report). Labels are not perfect. |
| `reference_features.parquet` | The host-hour feature table (a reference solution to Lecture 1 Exercise 5). Use it if you did not finish your own. |
| `malware_features.parquet` | Synthetic EMBER-style static features for 40,000 files: `sha256, first_seen, label, family, campaign` plus 48 features in six groups (`bytehist_*`, `byteent_*`, `str_*`, `hdr_*`, `sec_*`, `imp*`/`exp_*`). `family` is `benign` for label 0. `campaign` groups near-duplicate variants. |

The malware file is a stand-in with the same structure as EMBER, built to show the same effects (near-duplicate variants,
drift over time). If you have the real EMBER2018 vectorized features you may use a subsample instead. Say so in your report.

### Reference feature table columns
`src_ip, hour, n_alerts, n_sigs, n_dst, n_ports, sev_min, sev_mean, sig_rarity, offhours, dns_n, dns_ent_max, dns_len_max,
conn_n, conn_bytes_out, conn_n_dst, conn_max_pair, ioc_hit, crit`
