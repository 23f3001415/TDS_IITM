WITH hours AS (
    SELECT range AS hour
    FROM range(24)
),
hourly AS (
    SELECT
        EXTRACT(HOUR FROM CAST("timestamp" AS TIMESTAMP)) AS hour,
        category,
        SUM(amount) AS total_amount
    FROM sales
    GROUP BY 1, 2
)
SELECT
    h.hour,
    ROUND(COALESCE(SUM(CASE WHEN s.category = 'Clothing' THEN s.total_amount END), 0), 0) AS "Clothing",
    ROUND(COALESCE(SUM(CASE WHEN s.category = 'Home Goods' THEN s.total_amount END), 0), 0) AS "Home Goods",
    ROUND(COALESCE(SUM(CASE WHEN s.category = 'Electronics' THEN s.total_amount END), 0), 0) AS "Electronics"
FROM hours h
LEFT JOIN hourly s ON s.hour = h.hour
GROUP BY h.hour
ORDER BY h.hour;
