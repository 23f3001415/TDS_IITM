# Q4: Correlation Matrix with Excel Data Analysis ToolPak

## ELI15 Step-by-Step (Complete Beginner)

1. Open `q-correlation-excel.csv` in Excel.
2. Go to `Data` tab.
3. Click `Data Analysis` (enable Analysis ToolPak if missing).
4. Choose `Correlation` and click `OK`.
5. Select all 5 columns including headers:
   `Study_Hours, Sleep_Hours, Screen_Time, Attendance_Percent, Exam_Score`.
6. Tick `Labels in first row`.
7. Click `OK` to generate the 5x5 correlation matrix.
8. Ignore diagonal `1.0` values (self-correlation).
9. Find the largest positive off-diagonal correlation.
10. Submit in format:
    `Variable1, Variable2, 0.XXXX`

## Files in This Folder

- `q-correlation-excel.csv`: input file
- `solution.py`: script to compute the same Pearson matrix result
- `answer.txt`: final submission string

## Run (optional verification)

```powershell
cd C:\Users\sriva\OneDrive\Documents\TDS\ga5\q4
uv run solution.py
```

## Final Answer

`Study_Hours, Exam_Score, 0.8187`

