# Q7: Outlier Detection with Excel Z-Score Method

## ELI15 Step-by-Step (Complete Beginner)

1. Open `q-outlier-detection-excel.csv` in Excel.
2. Column A should contain `Delivery_Minutes` from `A2` to `A201`.
3. In `B2`, type:

```excel
=(A2 - AVERAGE($A$2:$A$201)) / STDEV($A$2:$A$201)
```

4. Copy `B2` down to `B201` (these are Z-scores).
5. In `C2`, type:

```excel
=IF(ABS(B2)>2,1,0)
```

6. Copy `C2` down to `C201`.
7. In any empty cell, type:

```excel
=SUM(C2:C201)
```

8. That sum is your outlier count.

Important:
- Use `STDEV` (sample standard deviation), not `STDEVP`.
- Count condition is strictly `|Z| > 2`.

## Files in This Folder

- `q-outlier-detection-excel.csv`: input data
- `solution.py`: equivalent script calculation
- `answer.txt`: final outlier count

## Run (optional verification)

```powershell
cd C:\Users\sriva\OneDrive\Documents\TDS\ga5\q7
uv run solution.py
```

## Final Answer

`9`

