# Question 1: Excel - Operational Margin Consolidation

## Final Answer (submit this)
`271431.32`

## ELI15 Step-by-Step (for a complete novice)
1. Open `q-excel-operational-metrics.xlsx` in Excel and go to `Operational Close`.
2. Convert the data into a Table (`Ctrl + T`).
3. Trim spaces in `Record ID` and `Region` using `TRIM(...)`.
4. Standardize `Region` to canonical names using a lookup table. For this dataset, treat all MEA aliases as `Middle East & Africa`, including:
   - `MEA`
   - `Middle East/Africa`
   - `MiddleEast&Africa`
   - `M. East Africa`
5. Parse `Closing Period` into real dates:
   - `YYYY-MM-DD` directly.
   - `DD/MM/YYYY` as day-first.
   - `Mon DD, YYYY` directly.
   - `YYYY Qn` as quarter-end (e.g., `2024 Q3` -> `30-Sep-2024`).
6. Clean `Revenue (reported)` and `Expense (reported)` by removing `USD`, `$`, commas, and spaces, then convert to number.
7. If Expense is blank or `USD TBD`, set Expense = `37%` of Revenue.
8. Extract first value from `Ops Notes` using `TEXTBEFORE([@[Ops Notes]],"|")` and call it `OpsCategory`.
9. Filter rows where:
   - `OpsCategory = Billing`
   - `Region = Middle East & Africa` (after alias standardization)
   - `ClosingDate <= 16-Apr-2024`
10. Compute `Variance = Revenue - Expense`.
11. Sum `Variance` for filtered rows.
12. Final total variance is **`271431.32`**.

## Validation snapshot
- Matching filtered rows: 12
- Computation rule: `SUM(Revenue_clean - Expense_final)`
