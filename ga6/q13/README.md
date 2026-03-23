# Q13: The Latency SLA Checker

## ELI15 Step-by-Step

1. Group requests by `endpoint`.
2. For each endpoint, compute:
   - `p50` with `PERCENTILE_CONT(0.50)`
   - `p95` with `PERCENTILE_CONT(0.95)`
   - `p99` with `PERCENTILE_CONT(0.99)`
   - `error_rate_pct` with `COUNT(*) FILTER (WHERE is_error = true) * 100.0 / COUNT(*)`
3. Then check all 4 SLA thresholds:
   - `p50 <= 80`
   - `p95 <= 400`
   - `p99 <= 800`
   - `error_rate_pct <= 2.0`
4. `sla_status` is `PASS` only if all 4 pass.
5. Build `violated_slas` by concatenating the failed metric names and trimming the trailing comma.

## Final DuckDB Query

```sql
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
```
