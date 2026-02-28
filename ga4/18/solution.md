# Question 18: DuckDB - Data Preparation for RetailCo Analytics

## Final Answer (submit this SQL)
```sql
WITH prepared AS (
    SELECT
        order_id,
        COALESCE(customer, 'Unknown') AS customer,
        amount,
        CASE
            WHEN amount > 720 THEN 'high'
            WHEN amount > 323 THEN 'medium'
            ELSE 'low'
        END AS price_band
    FROM orders
    WHERE region = 'LATAM'
)
SELECT
    COUNT(*) AS order_count,
    COALESCE(ROUND(SUM(amount), 2), 0) AS total_amount
FROM prepared
WHERE price_band = 'medium';
```

## ELI15 Step-by-Step (for a complete novice)
1. Start from `orders`.
2. Keep only rows where `region = 'LATAM'`.
3. Replace missing customer names with `COALESCE(customer, 'Unknown')`.
4. Create `price_band` using `CASE`:
   - `high` if amount > 720
   - `medium` if amount > 323
   - `low` otherwise
5. Keep only `price_band = 'medium'`.
6. Return one row with:
   - `order_count` = number of medium rows
   - `total_amount` = rounded sum of amount (2 decimals)
