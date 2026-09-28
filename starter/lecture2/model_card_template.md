# Model card: [name]  (two pages)
**Author / date / data used** (my own features.parquet or the reference file? synthetic EMBER stand-in or real EMBER?):

## 1. Purpose and decision supported
## 2. Data and labels (sources, delay, noise, what "unlabelled = benign" does)
## 3. Splits (dates, gap, positives per split, grouping)
## 4. Results (table: model, AP, TPR@0.1% FPR, precision@K, recall@K, each with a 95% host-bootstrap interval; baselines included)
## 5. Failure modes (drift after 8 March; malware drift over months; feedback loops)
## 6. Recommendation: ship / shadow mode / do not ship, and why
## 7. Pitfall audit (Arp et al., 2022). Name the TWO you are most exposed to and cite evidence from this work.
1 sampling bias · 2 label inaccuracy · 3 data snooping · 4 spurious correlations · 5 biased parameter selection ·
6 inappropriate baseline · 7 inappropriate measures · 8 base-rate fallacy · 9 lab-only evaluation · 10 inappropriate threat model
