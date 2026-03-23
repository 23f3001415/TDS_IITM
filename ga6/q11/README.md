# Q11: Train-Test Contamination Scanner

## ELI15 Step-by-Step (Complete Beginner)

1. You have two datasets:
   - `train.csv`
   - `test.csv`
2. A test row is called **leaked** if its feature values already appeared in training.
3. The feature columns are only:
   - `age`
   - `income`
   - `education`
   - `hours_per_week`
4. Do **not** use `label` for matching.
5. The easiest way to find leakage is `pandas.merge()`.
6. Keep only the feature columns from train.
7. Drop duplicate training feature rows so matching is clean.
8. Then merge test with train on the feature columns.
9. Use `indicator=True`.
10. That creates a special `_merge` column.
11. If `_merge == "both"`, that test row matched a training row.
12. Those are the leaked rows.
13. Then split the test set into:
   - leaked rows
   - clean rows
14. Accuracy is just the mean of `is_correct` times `100`.
15. So:
   - leaked accuracy = `leaked_rows["is_correct"].mean() * 100`
   - clean accuracy = `clean_rows["is_correct"].mean() * 100`
16. The question says reported accuracy is `76.5%`.
17. So inflation in percentage points is:
   - `76.5 - clean_accuracy`
18. Running the calculation on your downloaded files gives:
   - leaked count = `30`
   - leaked accuracy = `96.67`
   - clean accuracy = `72.94`
   - inflation = `3.56`

## Files in This Folder

- `train.csv`: copied from your Downloads folder
- `test.csv`: copied from your Downloads folder
- `solution.py`: contamination scanner
- `answer.txt`: final submission string

## Run

```powershell
cd C:\Users\sriva\OneDrive\Documents\TDS\ga6\q11
python solution.py
```

## Final Answer To Submit

```text
30,96.67,72.94,3.56
```
