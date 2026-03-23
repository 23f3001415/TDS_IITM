# Q7: The Threshold Engineer

## ELI15 Step-by-Step

1. Test every threshold from `0.05` to `0.95` in steps of `0.05`.
2. In DuckDB, generate them with `generate_series(5, 95, 5)` and divide by `100.0`.
3. `CROSS JOIN` pairs every threshold with every prediction row.
4. For each threshold, compute:
   - `tp`: `score >= t AND true_label = 1`
   - `fn`: `score < t AND true_label = 1`
   - `fp`: `score >= t AND true_label = 0`
5. Expected cost is:
   - `(7 * fn + fp) / total_rows`
6. Pick the threshold with the minimum expected cost.
7. Then compute precision and recall on that chosen row.

## Final DuckDB Query

```sql
WITH threshold_metrics AS (
    SELECT
        t AS threshold,
        COUNT(*) AS total_rows,
        SUM(CASE WHEN score >= t AND true_label = 1 THEN 1 ELSE 0 END) AS tp,
        SUM(CASE WHEN score < t AND true_label = 1 THEN 1 ELSE 0 END) AS fn,
        SUM(CASE WHEN score >= t AND true_label = 0 THEN 1 ELSE 0 END) AS fp,
        (
            7.0 * SUM(CASE WHEN score < t AND true_label = 1 THEN 1 ELSE 0 END)
            + SUM(CASE WHEN score >= t AND true_label = 0 THEN 1 ELSE 0 END)
        ) / COUNT(*) AS expected_cost
    FROM (
        SELECT generate_series / 100.0 AS t
        FROM generate_series(5, 95, 5)
    ) AS thresholds
    CROSS JOIN predictions
    GROUP BY t
),
best AS (
    SELECT *
    FROM threshold_metrics
    ORDER BY expected_cost ASC, threshold ASC
    LIMIT 1
)
SELECT
    threshold AS optimal_threshold,
    ROUND(tp * 1.0 / NULLIF(tp + fp, 0), 4) AS precision_at_threshold,
    ROUND(tp * 1.0 / NULLIF(tp + fn, 0), 4) AS recall_at_threshold,
    ROUND(expected_cost, 6) AS expected_cost_at_threshold
FROM best;
```
