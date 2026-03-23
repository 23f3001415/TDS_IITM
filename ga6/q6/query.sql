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
