# Q10: Geospatial Analysis - Nearest Warehouse Assignment

## ELI15 Step-by-Step (Complete Beginner)

1. Open `q-geospatial-nearest-warehouse.csv`.
2. Each row is one delivery location (latitude, longitude).
3. Keep warehouse locations fixed:
   - Delhi: `(28.6139, 77.209)`
   - Mumbai: `(19.076, 72.8777)`
   - Chennai: `(13.0827, 80.2707)`
4. For each delivery, compute Haversine distance to all 3 warehouses.
5. Pick the smallest distance -> that delivery is assigned to that warehouse.
6. Count assigned deliveries per warehouse.
7. Choose warehouse with maximum count.
8. Submit as: `Warehouse_Name, count`

## Files in This Folder

- `q-geospatial-nearest-warehouse.csv`: input data
- `solution.py`: Haversine + nearest warehouse assignment
- `assigned_deliveries.csv`: output with distance columns and assignment
- `answer.txt`: final busiest warehouse and count

## Run

```powershell
cd C:\Users\sriva\OneDrive\Documents\TDS\ga5\q10
uv run solution.py
```

## Final Answer

`Chennai, 23`

