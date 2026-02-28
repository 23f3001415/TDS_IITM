# Question 12: Shell - Parse and Aggregate Messy CSV Logs

## Final Answer (submit this)
`Beauty:2578906.57|Books:2589164.75|Clothing:2552225.33|Electronics:2632375.07|Furniture:2616516.09|Groceries:2623543.48|Sports:2605640.69|Toys:2603306.47`

## ELI15 Step-by-Step (for a complete novice)
1. Open the CSV file in shell.
2. Convert all `|` separators to `,` so every row has one common separator.
3. Split each row into fields.
4. Trim extra spaces around each field.
5. Ignore rows where category is missing.
6. Read `Amount` (3rd field) and `Category` (4th field).
7. Add amount into a running total per category.
8. Sort categories alphabetically.
9. Print output as:
   - `Category:Amount|Category:Amount|...`
10. Keep exactly 2 decimals for each amount.

## One-liner style command idea
```sh
awk 'NR>1{gsub(/\|/,",",$0); n=split($0,a,","); if(n<4)next; amt=a[3]; cat=a[4]; gsub(/^[ \t]+|[ \t]+$/,"",amt); gsub(/^[ \t]+|[ \t]+$/,"",cat); if(cat==""||amt!~/^-?[0-9]+([.][0-9]+)?$/)next; s[cat]+=amt} END{for(c in s) printf "%s:%0.2f\n",c,s[c]}' transactions.csv | sort | paste -sd'|' -
```

## Validation snapshot
- Total transaction rows processed (excluding header): 100135
- Rows kept after filtering missing category: 79993
- Categories aggregated: 8
