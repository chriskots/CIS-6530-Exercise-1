# Exercise 3: usage  awk -f ex3_ssh.awk auth.log > ssh_report.tsv
# Output header: src_ip  failures  distinct_users  first_fail  last_fail  success_after_fail  likely_compromise
# Tip: find fields by searching for the tokens "from" and "for" rather than fixed positions.
#      ("Failed password for invalid user X from IP ..." and "Failed password for X from IP ..." differ in length.)
/Failed password/ {
  # TODO: extract ip and user; count failures; count distinct users per ip; remember first/last time
}
/Accepted password/ {
  # TODO: order matters: was this address already over the failure threshold?
}
END {
  print "src_ip\tfailures\tdistinct_users\tfirst_fail\tlast_fail\tsuccess_after_fail\tlikely_compromise"
  # TODO: one row per ip with >= 10 failures
}
