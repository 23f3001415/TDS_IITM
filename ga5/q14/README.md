# Q14: Python - Multi-Depot Nearest Warehouse Assignment

## ELI15 Step-by-Step (Complete Beginner)

1. Load warehouse CSV (5 depots with lat/lon).
2. Load orders CSV (all orders with lat/lon).
3. For each order, compute distance to each warehouse using Haversine.
4. Pick the smallest distance (`nearest warehouse`) for that order.
5. Count how many orders each warehouse got.
6. Warehouse with the highest count is the answer.

## Files in This Folder

- `q-geospatial-python-closest-warehouses.csv`: warehouse locations
- `q-geospatial-python-closest-orders.csv`: order locations
- `solution.py`: nearest-warehouse assignment solver
- `assigned_orders.csv`: per-order assignment output
- `answer.txt`: final busiest warehouse and count

## Run

```powershell
cd C:\Users\sriva\OneDrive\Documents\TDS\ga5\q14
uv run solution.py
```

## Final Answer

`WH-05, 14`

