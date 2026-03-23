# Q11: Datasette - Top City by Delivered Revenue

## ELI15 Step-by-Step (Complete Beginner)

1. You have a SQL script file that creates and fills an `orders` table.
2. First create a SQLite database from that script.
3. Open it in Datasette:
   - `datasette q-datasette-sales-summary.db`
4. Open table `orders`.
5. Add a facet on `status` and click `delivered`.
6. Switch to SQL view.
7. Run:

```sql
SELECT city, SUM(quantity * unit_price) AS total_revenue
FROM orders
WHERE LOWER(status) = 'delivered'
GROUP BY city
ORDER BY total_revenue DESC
LIMIT 1;
```

8. The first row is the answer city.

## Files in This Folder

- `q-datasette-sales-summary.sql`: input SQL build script
- `q-datasette-sales-summary.db`: generated SQLite DB
- `solution.py`: builds DB and returns top city
- `answer.txt`: final city answer

## Run

```powershell
cd C:\Users\sriva\OneDrive\Documents\TDS\ga5\q11
uv run solution.py
```

## Final Answer

`Bangalore`

