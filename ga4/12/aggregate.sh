#!/usr/bin/env sh

# Usage:
# sh aggregate.sh /path/to/transactions.csv

FILE="$1"

awk '
BEGIN { FS="," }
NR==1 { next }                      # skip header
{
  gsub(/\|/, ",", $0)               # normalize separators: pipe -> comma
  n = split($0, a, ",")
  if (n < 4) next

  amount = a[3]
  category = a[4]

  gsub(/^[ \t]+|[ \t]+$/, "", amount)   # trim amount
  gsub(/^[ \t]+|[ \t]+$/, "", category) # trim category

  if (category == "") next               # drop missing categories
  if (amount !~ /^-?[0-9]+([.][0-9]+)?$/) next

  sum[category] += amount + 0
}
END {
  for (c in sum) {
    printf "%s:%0.2f\n", c, sum[c]
  }
}
' "$FILE" | sort | paste -sd'|' -
