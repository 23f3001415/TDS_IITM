WITH parsed AS (
    SELECT
        CASE
            WHEN sale_date LIKE '____-__-__' THEN STRPTIME(sale_date, '%Y-%m-%d')
            WHEN sale_date LIKE '__/__/____' THEN STRPTIME(sale_date, '%d/%m/%Y')
            WHEN sale_date LIKE '% __, ____' THEN STRPTIME(sale_date, '%B %d, %Y')
            ELSE NULL
        END::DATE AS sale_dt,
        amount
    FROM sales
),
monthly AS (
    SELECT
        DATE_TRUNC('month', sale_dt) AS month_start,
        SUM(amount) AS monthly_revenue
    FROM parsed
    WHERE sale_dt IS NOT NULL
      AND EXTRACT(YEAR FROM sale_dt) = 2024
    GROUP BY 1
),
mom AS (
    SELECT
        month_start,
        monthly_revenue,
        LAG(monthly_revenue) OVER (ORDER BY month_start) AS prev_month_revenue
    FROM monthly
)
SELECT
    STRFTIME(month_start, '%Y-%m') AS month,
    ROUND(((monthly_revenue - prev_month_revenue) / prev_month_revenue) * 100, 2) AS mom_growth_pct
FROM mom
WHERE prev_month_revenue IS NOT NULL
  AND prev_month_revenue <> 0
ORDER BY mom_growth_pct DESC
LIMIT 1;
