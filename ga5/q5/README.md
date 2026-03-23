# Q5: Multiple Linear Regression with Excel Data Analysis ToolPak

## ELI15 Step-by-Step (Complete Beginner)

1. Open `q-regression-excel.csv` in Excel.
2. Go to `Data` tab.
3. Click `Data Analysis` and choose `Regression`.
4. Set `Y Input Range` to `Price` (include header).
5. Set `X Input Range` to:
   `Area_SqFt, Bedrooms, Age_Years, Distance_City_Center_Km` (all 4 together, include headers).
6. Tick `Labels`.
7. Click `OK` and note coefficients:
   Intercept, Area, Bedrooms, Age, Distance.
8. Plug values into:
   `Intercept + Area*1800 + Bedrooms*3 + Age*10 + Distance*5`
9. Round to 2 decimals.
10. Submit only that number.

## Files in This Folder

- `q-regression-excel.csv`: input data
- `solution.py`: OLS regression equivalent to Excel ToolPak
- `answer.txt`: final predicted price

## Run (optional verification)

```powershell
cd C:\Users\sriva\OneDrive\Documents\TDS\ga5\q5
uv run solution.py
```

## Final Answer

`401030.97`

