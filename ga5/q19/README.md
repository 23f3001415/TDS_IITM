# Q19: Weighted Moving Average - Regional Revenue Analysis

## ELI15 Step-by-Step (Complete Beginner)

1. Open `q-wma-regional-sales.csv`.
2. Filter `Region = East` only.
3. Sort by `Week` ascending.
4. Take East revenues for weeks `22, 23, 24, 25, 26`.
5. Apply weights `[1, 2, 3, 4, 5]` (oldest to newest):

```text
WMA = (1*W22 + 2*W23 + 3*W24 + 4*W25 + 5*W26) / 15
```

6. Round to 2 decimals and submit.

## East Revenue Values Used

- Week 22: 37637.10
- Week 23: 38228.76
- Week 24: 45299.40
- Week 25: 43362.15
- Week 26: 48471.06

## Files in This Folder

- `q-wma-regional-sales.csv`: input data
- `solution.py`: East-region WMA calculator
- `east_weeks_22_26.csv`: extracted rows used in computation
- `answer.txt`: final WMA value

## Run

```powershell
cd C:\Users\sriva\OneDrive\Documents\TDS\ga5\q19
uv run solution.py
```

## Final Answer

`44386.45`

