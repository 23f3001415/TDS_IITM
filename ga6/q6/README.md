# Q6: The Slice Detective

## ELI15 Step-by-Step

1. A slice means a subgroup like `platform = mobile` or `platform = mobile, language_detected = fr`.
2. You must test all 3 one-column slices and all 3 two-column combinations.
3. For each slice, compute:
   - `slice_size = COUNT(*)`
   - `slice_accuracy = AVG(CASE WHEN true_label = predicted_label THEN 1.0 ELSE 0.0 END)`
4. Keep only slices with at least `38` rows, so use `HAVING COUNT(*) >= 38`.
5. Compute the overall accuracy once in a separate CTE.
6. Stack all candidate slice queries with `UNION ALL`.
7. Keep only slices that are at least `0.40` below overall accuracy.
8. Sort by `slice_accuracy ASC` and take `LIMIT 1`.

## Final DuckDB Query

```sql
WITH overall AS (
    SELECT AVG(CASE WHEN true_label = predicted_label THEN 1.0 ELSE 0.0 END) AS overall_accuracy
    FROM predictions
),
all_slices AS (
    SELECT
        'platform = ' || platform AS slice_definition,
        COUNT(*) AS slice_size,
        AVG(CASE WHEN true_label = predicted_label THEN 1.0 ELSE 0.0 END) AS slice_accuracy
    FROM predictions
    GROUP BY platform
    HAVING COUNT(*) >= 38

    UNION ALL

    SELECT
        'language_detected = ' || language_detected AS slice_definition,
        COUNT(*) AS slice_size,
        AVG(CASE WHEN true_label = predicted_label THEN 1.0 ELSE 0.0 END) AS slice_accuracy
    FROM predictions
    GROUP BY language_detected
    HAVING COUNT(*) >= 38

    UNION ALL

    SELECT
        'message_length_bucket = ' || message_length_bucket AS slice_definition,
        COUNT(*) AS slice_size,
        AVG(CASE WHEN true_label = predicted_label THEN 1.0 ELSE 0.0 END) AS slice_accuracy
    FROM predictions
    GROUP BY message_length_bucket
    HAVING COUNT(*) >= 38

    UNION ALL

    SELECT
        'platform = ' || platform || ', language_detected = ' || language_detected AS slice_definition,
        COUNT(*) AS slice_size,
        AVG(CASE WHEN true_label = predicted_label THEN 1.0 ELSE 0.0 END) AS slice_accuracy
    FROM predictions
    GROUP BY platform, language_detected
    HAVING COUNT(*) >= 38

    UNION ALL

    SELECT
        'platform = ' || platform || ', message_length_bucket = ' || message_length_bucket AS slice_definition,
        COUNT(*) AS slice_size,
        AVG(CASE WHEN true_label = predicted_label THEN 1.0 ELSE 0.0 END) AS slice_accuracy
    FROM predictions
    GROUP BY platform, message_length_bucket
    HAVING COUNT(*) >= 38

    UNION ALL

    SELECT
        'language_detected = ' || language_detected || ', message_length_bucket = ' || message_length_bucket AS slice_definition,
        COUNT(*) AS slice_size,
        AVG(CASE WHEN true_label = predicted_label THEN 1.0 ELSE 0.0 END) AS slice_accuracy
    FROM predictions
    GROUP BY language_detected, message_length_bucket
    HAVING COUNT(*) >= 38
)
SELECT
    s.slice_definition,
    s.slice_size,
    s.slice_accuracy,
    o.overall_accuracy
FROM all_slices AS s
CROSS JOIN overall AS o
WHERE s.slice_accuracy <= o.overall_accuracy - 0.40
ORDER BY s.slice_accuracy ASC
LIMIT 1;
```
