WITH metrics AS (
    SELECT
        endpoint,
        ROUND(PERCENTILE_CONT(0.50) WITHIN GROUP (ORDER BY latency_ms), 2) AS p50_ms,
        ROUND(PERCENTILE_CONT(0.95) WITHIN GROUP (ORDER BY latency_ms), 2) AS p95_ms,
        ROUND(PERCENTILE_CONT(0.99) WITHIN GROUP (ORDER BY latency_ms), 2) AS p99_ms,
        ROUND(COUNT(*) FILTER (WHERE is_error = true) * 100.0 / COUNT(*), 2) AS error_rate_pct
    FROM api_logs
    GROUP BY endpoint
)
SELECT
    endpoint,
    p50_ms,
    p95_ms,
    p99_ms,
    error_rate_pct,
    CASE
        WHEN p50_ms <= 80
         AND p95_ms <= 400
         AND p99_ms <= 800
         AND error_rate_pct <= 2.0
        THEN 'PASS'
        ELSE 'FAIL'
    END AS sla_status,
    RTRIM(
        CASE WHEN p50_ms > 80 THEN 'p50,' ELSE '' END ||
        CASE WHEN p95_ms > 400 THEN 'p95,' ELSE '' END ||
        CASE WHEN p99_ms > 800 THEN 'p99,' ELSE '' END ||
        CASE WHEN error_rate_pct > 2.0 THEN 'error_rate,' ELSE '' END,
        ','
    ) AS violated_slas
FROM metrics
ORDER BY endpoint ASC;
