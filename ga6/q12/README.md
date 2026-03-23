# Q12: The Idempotency Prober

## ELI15 Step-by-Step (Complete Beginner)

1. You are given:
   - a CSV with 100 rows
   - a preprocessing function
2. The function does two things:
   - clips numeric columns between their 10th and 90th percentiles
   - fills missing values using forward-fill and backward-fill
3. You must test 3 properties.

## 1. Idempotency

4. Idempotency means:
   - running the function once and running it twice should give the same result
   - in math words: `f(f(x)) = f(x)`
5. So:
   - run `result1 = preprocess(df, "value_a")`
   - run `result2 = preprocess(result1, "value_a")`
6. Then compare each row of `result1` and `result2`.
7. If **any** column in a row changed, that row violates idempotency.
8. For float columns, use tolerance `1e-9`.
9. On this dataset, the count is:
   - `28`

## 2. Monotonicity

10. The monotonicity column here is `value_a`.
11. To avoid double-counting pairs, use a normal pair loop with `i < j`.
12. For each such pair:
   - skip it if either original `value_a` is null
   - check whether original `value_a[i] > value_a[j]`
13. If that original strict ordering holds, then the processed output must still satisfy:
   - `processed_value_a[i] > processed_value_a[j]`
14. If clipping turns those two rows into a tie, that still breaks the strict ordering and counts as a violation.
15. On this dataset, the count is:
   - `48`

## 3. Null Stability

16. If an input row had no nulls, the output row should also have no nulls.
17. Check each row:
   - if input row null count is `0`
   - but output row null count is greater than `0`
   - then it is a violation
18. Because the preprocessing fills missing values and does not create new nulls here, the count is:
   - `0`

## Files in This Folder

- `records.csv`: copied from your Downloads folder
- `solution.py`: property checker
- `answer.txt`: final submission string

## Run

```powershell
cd C:\Users\sriva\OneDrive\Documents\TDS\ga6\q12
python solution.py
```

## Final Answer To Submit

```text
28,48,0
```
