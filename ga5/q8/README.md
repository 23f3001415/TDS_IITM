# Q8: Data Analysis with Python - 21-Day Exponential Moving Average

## ELI15 Step-by-Step (Complete Beginner)

1. Open `q-stock-prices-ema.csv` (it has Date, Ticker, Close_Price).
2. Convert `Date` to real date values.
3. Sort by `Ticker` and `Date` so each stock is in time order.
4. For each ticker separately, compute:
   `EMA_21 = ewm(span=21, adjust=False).mean()`
5. Find the latest date in the dataset.
6. Keep only rows for that latest date (one row per ticker).
7. Compare their `EMA_21` values.
8. Pick the highest EMA and its ticker.
9. Round EMA to 2 decimals.
10. Submit in format: `EMA_value, TICKER`

## Files in This Folder

- `q-stock-prices-ema.csv`: input stock data
- `solution.py`: EMA calculator and winner finder
- `answer.txt`: final submission string

## Run

```powershell
cd C:\Users\sriva\OneDrive\Documents\TDS\ga5\q8
uv run solution.py
```

## Final Answer

`368.20, META`

