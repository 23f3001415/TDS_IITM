# Q6: Seasonal Forecasting with Excel `FORECAST.ETS`

## ELI15 Step-by-Step (Complete Beginner)

1. Open `q-forecasting-excel.csv` in Excel.
2. Make sure:
   - Column A = `Month` (1 to 36)
   - Column B = `Visitors`
3. Click any empty cell (for example `C2`).
4. Type this exact formula:

```excel
=FORECAST.ETS(37, B2:B37, A2:A37, 12)
```

5. Press Enter.
6. Excel gives the forecast for Month 37.
7. Round to nearest whole number (if needed).
8. Submit that integer.

## Why this works (super simple)

- `FORECAST.ETS` learns trend + repeating yearly season pattern.
- `12` means one full season is 12 months.
- So Excel uses months 1–36 to predict month 37.

## Final Answer

`16754`

