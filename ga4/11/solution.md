# Question 11: FastAPI Batch Sentiment Analysis

## Final Answer (submit this FastAPI URL)
`https://screenshot-ontario-smithsonian-connection.trycloudflare.com/sentiment`

This endpoint now includes CORS support for browser-based graders.

## ELI15 Step-by-Step (for a complete novice)
1. Create a FastAPI app file (`main.py`).
2. Make a `POST /sentiment` endpoint.
3. Input format must be:
   - `{"sentences": ["I love this!", "I'm sad."]}`
4. For each sentence, predict one label from:
   - `happy`, `sad`, or `neutral`
5. Return output in the same order:
   - `{"results":[{"sentence":"I love this!","sentiment":"happy"}, ...]}`
6. Run server:
   - `python -m uvicorn main:app --host 0.0.0.0 --port 8000`
7. Expose server publicly (needed for grader):
   - `cloudflared tunnel --url http://localhost:8000 --no-autoupdate`
8. Copy the public URL and append `/sentiment`, then submit it.

## Files
- [main.py](C:\Users\sriva\OneDrive\Documents\TDS\ga4\11\main.py)
- [requirements.txt](C:\Users\sriva\OneDrive\Documents\TDS\ga4\11\requirements.txt)
- [start_server.ps1](C:\Users\sriva\OneDrive\Documents\TDS\ga4\11\start_server.ps1)
- [stop_server.ps1](C:\Users\sriva\OneDrive\Documents\TDS\ga4\11\stop_server.ps1)
