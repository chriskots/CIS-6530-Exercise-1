# Exercise 4, step 1: usage  awk -F'\t' -f ex4_deltas.awk conn.log > deltas.tsv
# Output header: pair  delta_s  orig_bytes      pair = orig_h ">" resp_h ":" resp_p
# Remember: skip lines starting with "#"; "-" means unset (do not compare it as a number).
BEGIN { OFS = "\t"; print "pair", "delta_s", "orig_bytes" }
# TODO
