# Q13 - FastAPI Server to Serve CSV Data (ELI15 Guide)

Think of FastAPI as a small waiter app:
- CSV file = kitchen notebook
- `/api` = counter where people ask for data
- `?class=...` = filter request like "give only these classes"

## What this question needs
1. Read `q-fastapi.csv` (columns: `studentId`, `class`).
2. Serve all rows at `/api` in same order as CSV.
3. If query has `class`, return only matching classes.
4. Keep original CSV row order in response.
5. Enable CORS so GET works from any origin.

## Files created
- `ga2/q13/q-fastapi.csv`
- `ga2/q13/app.py`
- `ga2/q13/requirements.txt`

## Step-by-step for complete novice
1. Open terminal in `ga2/q13` folder.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Start server:

```bash
uvicorn app:app --reload
```

4. Open this URL in browser:

```text
http://127.0.0.1:8000/api
```

You should get JSON like:

```json
{
  "students": [
    {"studentId": 1, "class": "5D"},
    {"studentId": 2, "class": "2S"}
  ]
}
```

5. Test filtering by one class:

```text
http://127.0.0.1:8000/api?class=5D
```

6. Test filtering by multiple classes:

```text
http://127.0.0.1:8000/api?class=5D&class=2S
```

## Why this solution is correct
- It reads CSV once and preserves row order.
- It filters by any number of `class` query values.
- It exposes endpoint exactly at `/api`.
- CORS middleware is enabled for GET from any origin.

## Final answer to submit for this question
`http://127.0.0.1:8000/api`