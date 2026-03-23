# Q20: Server Log Anomaly Detection - API Scraper

## ELI15 Step-by-Step (Complete Beginner)

1. Open `server_access_logs.csv`.
2. Keep only rows where:
   - `status_code == 429`
   - `endpoint == "/api/pricing"`
3. Count rows by `ip_address`.
4. IP with highest count is the scraper IP.
5. Now take **all rows** from that IP (not just 429 rows).
6. Compute median of `response_time_ms`.
7. Submit in format: `IP_ADDRESS, MEDIAN_MS`

## Files in This Folder

- `server_access_logs.csv`: input logs
- `solution.py`: scraper IP + median profiler
- `answer.txt`: final submission string

## Run

```powershell
cd C:\Users\sriva\OneDrive\Documents\TDS\ga5\q20
uv run solution.py
```

## Final Answer

`18.148.240.156, 180.3`

