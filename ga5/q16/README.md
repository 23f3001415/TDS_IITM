# Q16: DuckDB - Sales Over Time Pivot by Hour

## ELI15 Step-by-Step (Complete Beginner)

1. Create a list of all hours `0..23`.
2. Get the list of categories from `sales`.
3. Make every hour-category pair using `CROSS JOIN`.
4. `LEFT JOIN` real sales to those pairs and `SUM(amount)`.
   - Missing pairs become `0` using `COALESCE`.
5. Pivot rows into columns using `SUM(CASE WHEN ...)` (works on older DuckDB too).
6. Round totals to nearest integer with `ROUND(..., 0)`.
7. Sort by `hour`.

## Query File

- `query.sql` contains the full answer query.
