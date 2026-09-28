# Reproduce every Lecture 1 output from the raw data. Fill in the scripts, then run: make all
DATA ?= ../../data/lecture1
OUT  ?= ../../out
.PHONY: all clean
all: $(OUT)/alerts.csv $(OUT)/enriched.ndjson $(OUT)/ssh_report.tsv $(OUT)/beacons.csv $(OUT)/features.parquet $(OUT)/ranked.csv
$(OUT):
	mkdir -p $(OUT)
$(OUT)/alerts.csv: ex1_alerts.sh $(DATA)/eve.json | $(OUT)
	DATA=$(DATA) OUT=$(OUT) bash ex1_alerts.sh
$(OUT)/enriched.ndjson: ex2_flatten.sh $(DATA)/eve.json $(DATA)/iocs.json | $(OUT)
	DATA=$(DATA) OUT=$(OUT) bash ex2_flatten.sh
$(OUT)/ssh_report.tsv: ex3_ssh.awk $(DATA)/auth.log | $(OUT)
	awk -f ex3_ssh.awk $(DATA)/auth.log > $@
$(OUT)/deltas.tsv: ex4_deltas.awk $(DATA)/conn.log | $(OUT)
	awk -F'\t' -f ex4_deltas.awk $(DATA)/conn.log > $@
$(OUT)/beacons.csv: ex4_beacons.py $(OUT)/deltas.tsv
	OUT=$(OUT) python3 ex4_beacons.py
$(OUT)/features.parquet: ex5_features.py $(DATA)/eve.json $(DATA)/conn.log | $(OUT)
	DATA=$(DATA) OUT=$(OUT) python3 ex5_features.py
$(OUT)/ranked.csv: ex6_baselines.py $(OUT)/features.parquet
	OUT=$(OUT) python3 ex6_baselines.py
clean:
	rm -f $(OUT)/*
