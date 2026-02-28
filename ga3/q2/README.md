# Q2: LLM Structured Output - FastAPI Sentiment Analysis

## ELI15 Step-by-Step (Beginner Friendly)

1. Open PowerShell in `ga3/q2`.
2. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```
3. Set your OpenAI key in the same terminal window:
   ```powershell
   $env:OPENAI_API_KEY="your_openai_api_key_here"
   ```
4. Start API + tunnel in one command:
   ```powershell
   .\start_all.ps1
   ```
5. It prints:
   - `FINAL_ENDPOINT=https://....trycloudflare.com/comment`
6. Submit that `FINAL_ENDPOINT` URL to grader.
7. Quick test:
   ```powershell
   $url = Get-Content .\endpoint_url.txt
   Invoke-RestMethod -Method POST -Uri $url -ContentType "application/json" -Body '{"comment":"This product is amazing!"}'
   ```
8. Expected JSON shape:
   ```json
   {
     "sentiment": "positive",
     "rating": 5
   }
   ```

## If You Prefer Manual Steps

1. Terminal A:
   ```powershell
   $env:OPENAI_API_KEY="your_openai_api_key_here"
   python -m uvicorn main:app --host 0.0.0.0 --port 8000
   ```
2. Terminal B:
   ```powershell
   cloudflared tunnel --url http://localhost:8000 --no-autoupdate
   ```
3. Use `https://<random>.trycloudflare.com/comment`.

## Common Errors and Fixes

- `ERROR: [Errno 10048] ... address already in use`
  - Port 8000 already has another server.
  - Run:
    ```powershell
    .\stop_all.ps1
    .\start_all.ps1
    ```

- `OPENAI_API_KEY` seems ignored
  - You set it in one terminal but ran API in another terminal.
  - Set the key in the same terminal where you run `start_all.ps1`.

- Cloudflared shows `Cannot determine default origin certificate path ... cert.pem`
  - This is normal for quick tunnels and can be ignored.
  - It still works when a `https://...trycloudflare.com` URL is printed.

- Browser/frontend calls fail with CORS/OPTIONS issues
  - Already fixed in `main.py` using CORS middleware.

## What This Code Does

- Accepts request body:
  ```json
  {"comment":"..."}
  ```
- Calls OpenAI `gpt-4.1-mini` with `response_format` using strict JSON schema.
- Enforces response fields:
  - `sentiment`: `positive | negative | neutral`
  - `rating`: integer `1..5`
- Returns `application/json`.
- Handles invalid input and API failures gracefully.

## Files

- `main.py`: FastAPI app with `POST /comment`
- `requirements.txt`: dependencies
- `start_api.ps1`: starts API safely and writes PID/logs
- `start_tunnel.ps1`: starts Cloudflare tunnel and captures URL
- `start_all.ps1`: runs both and prints final endpoint
- `stop_all.ps1`: stops tracked/local q2 processes

## Final Answer (for grader)

Read from:

`endpoint_url.txt`

Current run endpoint:

`https://stranger-oxide-theory-container.trycloudflare.com/comment`
