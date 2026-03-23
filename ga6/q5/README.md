# Q5: Data Contract Violation Detector

## ELI15 Step-by-Step (Complete Beginner)

1. You have two CSV files:
   - `Day 1`: clean data
   - `Day 2`: corrupted data
2. Your job is to learn the rules from Day 1 and check which Day 2 rows break them.
3. A row is counted once even if it breaks many rules.
4. So the safest way is to keep a Python `set()` called `bad_rows`.
5. A set automatically avoids duplicates.
6. For each column, we apply the rules in this order:
   - null rule
   - numeric rule
   - date rule
   - categorical rule
7. First rule:
   - if Day 1 has `0` nulls in a column
   - then any null in Day 2 for that column is anomalous
8. Next, try numeric detection:
   - convert Day 1 values with `pd.to_numeric(..., errors="coerce")`
   - if more than `95%` parse successfully, treat the column as numeric
9. For numeric columns:
   - compute Day 1 minimum and maximum
   - flag any Day 2 value below the min or above the max
10. If the column is not numeric, try date detection:
   - convert Day 1 values with `pd.to_datetime(..., errors="coerce")`
   - if more than `90%` parse successfully, treat the column as date
11. For date columns:
   - flag any Day 2 date after today
12. If the column is neither numeric nor date, check whether it is categorical:
   - if Day 1 has `20` or fewer distinct non-null values
13. For categorical columns:
   - flag any Day 2 value that never appeared in Day 1
14. If a column becomes numeric, we stop there for that column.
15. If it becomes date, we do not also check it as categorical.
16. After all columns are processed, print `len(bad_rows)`.
17. Running the script on your downloaded files gives:
   - `66`

## Files in This Folder

- `day1.csv`: copied from your Downloads folder
- `day2.csv`: copied from your Downloads folder
- `solution.py`: validator script
- `answer.txt`: final submission number

## Run

```powershell
cd C:\Users\sriva\OneDrive\Documents\TDS\ga6\q5
python solution.py
```

## Final Answer To Submit

```text
66
```
