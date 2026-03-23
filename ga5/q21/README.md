# Q21: Rideshare Geospatial Revenue Analysis

## ELI15 Step-by-Step (Complete Beginner)

1. Load `rideshare_trips.csv`.
2. Convert `start_time` to datetime.
3. Keep only peak-hour trips:
   - hour >= 17
   - hour < 21
4. For each remaining trip, compute Haversine distance between pickup and dropoff.
5. Keep only trips with distance strictly greater than 7 km.
6. Group by `driver_id` and sum `fare_amount`.
7. Driver with the highest total fare is the answer.

## Files in This Folder

- `rideshare_trips.csv`: input trips
- `solution.py`: full filter + distance + aggregation pipeline
- `qualifying_trips.csv`: trips that passed both filters
- `answer.txt`: final `DRIVER_ID, TOTAL_FARE`

## Run

```powershell
cd C:\Users\sriva\OneDrive\Documents\TDS\ga5\q21
uv run solution.py
```

## Final Answer

`DRV-011, 468.85`

