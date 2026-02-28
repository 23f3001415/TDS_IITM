# Question 8: Parse Partial JSON

## Final Answer (submit this)
`53338`

## ELI15 Step-by-Step (for a complete novice)
1. Open `q-parse-partial-json.jsonl`.
2. Read the file line-by-line (100 lines total).
3. Each line may be broken at the end, so normal JSON parsing can fail.
4. Instead of parsing full JSON, extract just the `sales` number from each line.
5. Use a regex like `"sales":<number>` to recover values safely.
6. Convert each recovered value to a number.
7. Add all 100 `sales` values.
8. Final total sales is **`53338`**.

## Validation snapshot
- Total rows: 100
- Rows with recovered `sales`: 100
- Total sales: 53338
