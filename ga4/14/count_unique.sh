#!/usr/bin/env sh

# Usage:
# sh count_unique.sh /path/to/addresses.txt

FILE="$1"

COUNT=$(
  sed -E 's/^Address:[[:space:]]*//I; s/[[:space:]]*\(VALID\)[[:space:]]*$//I' "$FILE" \
  | tr '[:lower:]' '[:upper:]' \
  | sed -E 's/[^A-Z0-9 ]/ /g; s/[[:space:]]+/ /g; s/^ //; s/ $//' \
  | sort -u \
  | wc -l \
  | tr -d ' '
)

echo "unique_addresses:$COUNT"
