# Q18 Build a FastAPI File Validation Service (ELI15, Complete Beginner)

Think of this API like a security guard for uploaded files.

The guard checks 3 things before letting a file in:
1. Secret token in header.
2. Allowed file type.
3. File size limit.

If all checks pass and file is CSV, it reads the file and calculates stats.

## What this endpoint validates
- Header must be exactly:
  - `X-Upload-Token-4193: wrbu8ux9frfk15td`
- File extension allowed: `.csv`, `.json`, `.txt`
- Max file size: `63KB` (`64512` bytes)
- Upload field name: `file` (`multipart/form-data`)

## Error codes used
- `401 Unauthorized` -> token missing/wrong
- `400 Bad Request` -> wrong file type / malformed CSV
- `413 Payload Too Large` -> file exceeds 63KB

## Files in this solution
- `ga2/q18/api/index.py` -> FastAPI app
- `ga2/q18/requirements.txt` -> Python dependencies
- `ga2/q18/vercel.json` -> Vercel routing/build
- `ga2/q18/ELI15_q18_solution.md` -> this guide

## Step-by-step for a complete novice
1. Open terminal in `ga2/q18`.
2. Deploy to Vercel:
```bash
vercel --prod
```
3. Vercel gives URL like:
```text
https://your-project.vercel.app
```
4. Your endpoint is:
```text
https://your-project.vercel.app/api
```

## Test command (with the provided CSV)
```bash
curl -X POST "https://q18-three.vercel.app/api" \
  -H "X-Upload-Token-4193: wrbu8ux9frfk15td" \
  -F "file=@q-fastapi-file-validation.csv"
```

## Expected output for the provided CSV
```json
{
  "email": "23f3001415@ds.study.iitm.ac.in",
  "filename": "q-fastapi-file-validation.csv",
  "rows": 37,
  "columns": ["id", "name", "value", "category"],
  "totalValue": 18434.56,
  "categoryCounts": {"C": 12, "B": 10, "A": 6, "D": 9}
}
```

## Final endpoint URL for submission
`https://q18-three.vercel.app/api`
