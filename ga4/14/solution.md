# Question 14: Shell - Deduplicate and Aggregate Semi-Structured Address Data

## Final Answer (submit this)
`unique_addresses:1361`

## ELI15 Step-by-Step (for a complete novice)
1. Read the text file line-by-line.
2. Remove extra wrapper text:
   - Remove prefix `Address:`
   - Remove suffix `(VALID)`
3. Normalize formatting:
   - Convert to one case (UPPERCASE)
   - Remove punctuation
   - Collapse multiple spaces to a single space
4. Now each line is a canonical core address.
5. Sort all canonical lines.
6. Deduplicate with `sort -u`.
7. Count unique lines.
8. Output exactly as:
   - `unique_addresses:1361`

## Shell command pattern
```sh
sed -E 's/^Address:[[:space:]]*//I; s/[[:space:]]*\(VALID\)[[:space:]]*$//I' addresses.txt \
| tr '[:lower:]' '[:upper:]' \
| sed -E 's/[^A-Z0-9 ]/ /g; s/[[:space:]]+/ /g; s/^ //; s/ $//' \
| sort -u | wc -l
```
