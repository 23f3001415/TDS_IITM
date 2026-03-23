# Q12: DuckDB - Month with Highest Revenue Growth

## ELI15 Step-by-Step (Complete Beginner)

1. Your `sale_date` column is text, not a clean date.
2. Dates come in 3 different formats, so first detect format with `CASE`.
3. Parse with `STRPTIME` using:
   - `%Y-%m-%d`
   - `%d/%m/%Y`
   - `%B %d, %Y`
4. Keep only rows from year 2024.
5. Group by month and sum `amount` to get monthly revenue.
6. Use `LAG(monthly_revenue)` to fetch previous month revenue.
7. Compute growth:
   `((current - previous) / previous) * 100`
8. Round to 2 decimals.
9. Sort by growth descending and return top 1 month.

## Query File

- `query.sql` contains the exact DuckDB SQL to submit.
