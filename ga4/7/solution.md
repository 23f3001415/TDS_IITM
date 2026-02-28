# Question 7: JSON - Flatten Nested Customer Orders

## Final Answer (submit this)
`38`

## ELI15 Step-by-Step (for a complete novice)
1. Open `q-json-customer-flatten.jsonl`.
2. Read it line-by-line (streaming), not all at once.
3. For each customer record, open the `orders` array.
4. For each order, open the `items` array (this is the flatten step).
5. Keep only rows where:
   - `region = Asia Pacific`
   - `order_date` is between `2024-04-27` and `2024-06-01`
   - `channel = Reseller`
   - `category = Collaboration`
6. From matching item rows, take `quantity`.
7. Add all matching quantities.
8. Total quantity is **`38`**.

## Validation snapshot
- Matching flattened item rows: 7
- Total quantity: 38
