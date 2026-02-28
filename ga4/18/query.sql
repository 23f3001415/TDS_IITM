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
