# Q9: Geospatial Analysis - Haversine Distance and Correlation

## ELI15 Step-by-Step (Complete Beginner)

1. Open `q-geospatial-haversine-correlation.csv`.
2. Each row is one store with latitude, longitude, and monthly revenue.
3. Compute distance from HQ (New Delhi): `(28.6139, 77.209)` using Haversine formula.
4. Save that as a new column `Distance_Km`.
5. Compute Pearson correlation between `Distance_Km` and `Monthly_Revenue`.
6. Round to 4 decimals.
7. Submit only that number.

## Excel version

1. Put Haversine formula in `E2` and fill down to `E31`.
2. In empty cell, use:

```excel
=CORREL(E2:E31, D2:D31)
```

3. Round result to 4 decimals.

## Files in This Folder

- `q-geospatial-haversine-correlation.csv`: input data
- `solution.py`: Haversine + Pearson correlation script
- `with_distance.csv`: output with calculated `Distance_Km`
- `answer.txt`: final rounded correlation

## Run

```powershell
cd C:\Users\sriva\OneDrive\Documents\TDS\ga5\q9
uv run solution.py
```

## Final Answer

`-0.7991`

