# Q8: The Flaky Test Finder

## ELI15 Step-by-Step

1. A flaky test is not “fails on one commit and passes on another”.
2. It is only flaky when the **same commit** has both `PASS` and `FAIL` for the same test.
3. So first group by `(test_name, commit_hash)`.
4. For each `(test, commit)` pair, count:
   - passes
   - fails
   - total runs
5. A commit is flaky for that test when `passes > 0 AND fails > 0`.
6. Then group again by `test_name`.
7. Compute:
   - `flaky_commits`
   - `total_commits`
   - `total_passes`
   - `total_runs`
8. Final metrics:
   - `pass_rate = total_passes / total_runs`
   - `flakyness_score = flaky_commits / total_commits`
9. Keep only tests with `flaky_commits > 0`.

## Final DuckDB Query

```sql
WITH per_commit AS (
    SELECT
        test_name,
        commit_hash,
        COUNT(*) FILTER (WHERE outcome = 'PASS') AS passes,
        COUNT(*) FILTER (WHERE outcome = 'FAIL') AS fails,
        COUNT(*) AS total_runs
    FROM test_runs
    GROUP BY test_name, commit_hash
),
per_test AS (
    SELECT
        test_name,
        SUM(CASE WHEN passes > 0 AND fails > 0 THEN 1 ELSE 0 END) AS flaky_commits,
        COUNT(*) AS total_commits,
        SUM(passes) AS total_passes,
        SUM(total_runs) AS total_runs
    FROM per_commit
    GROUP BY test_name
)
SELECT
    test_name,
    flaky_commits,
    ROUND(total_passes * 1.0 / total_runs, 4) AS pass_rate,
    ROUND(flaky_commits * 1.0 / total_commits, 4) AS flakyness_score
FROM per_test
WHERE flaky_commits > 0
ORDER BY flakyness_score DESC, test_name ASC;
```
