# Q14 - Deploy a POST Analytics Endpoint to Vercel (ELI15 Guide)

Imagine you have latency report cards from many regions.
This endpoint reads those report cards and answers:
- average latency
- 95th percentile latency (p95)
- average uptime
- how many times latency crossed your threshold

## Input you must support
POST body:

```json
{"regions": ["amer", "apac"], "threshold_ms": 170}
```

## Output shape used here
This solution returns one object per region:

```json
{
  "amer": {
    "avg_latency": 157.30916666666664,
    "p95_latency": 206.904,
    "avg_uptime": 98.24933333333333,
    "breaches": 5
  },
  "apac": {
    "avg_latency": 155.35999999999999,
    "p95_latency": 203.20549999999997,
    "avg_uptime": 98.433,
    "breaches": 4
  }
}
```

(Order does not matter.)

## Files in this repo
- `ga2/q14/q-vercel-latency.json`
- `ga2/q14/api/index.py`
- `ga2/q14/requirements.txt`
- `ga2/q14/vercel.json`

## Step-by-step (beginner)
1. Open terminal in `ga2/q14`.
2. Deploy to Vercel:

```bash
vercel --prod
```

3. If prompted, login and link project.
4. After deploy, Vercel prints a URL like:

```text
https://your-project-name.vercel.app
```

5. Your POST endpoint is:

```text
https://your-project-name.vercel.app/api
```

6. Test with:

```bash
curl -X POST "https://your-project-name.vercel.app/api" \
  -H "Content-Type: application/json" \
  -d '{"regions":["amer","apac"],"threshold_ms":170}'
```

## CORS
CORS is enabled for POST from any origin in `api/index.py`.

## Final answer format to submit
`https://q14-dun.vercel.app/api`