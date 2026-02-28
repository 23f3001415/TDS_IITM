# Q3: Code Interpreter with AI Error Analysis

## ELI15 Step-by-Step (Beginner Friendly)

1. Open PowerShell in `ga3/q3`.
2. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```
3. Set Gemini API key in the same terminal (optional but recommended):
   ```powershell
   $env:GEMINI_API_KEY="your_gemini_api_key_here"
   ```
4. Start API + tunnel in one command:
   ```powershell
   .\start_all.ps1
   ```
5. It prints:
   - `FINAL_ENDPOINT=https://....trycloudflare.com/code-interpreter`
6. Submit that URL to grader.
7. Quick test:
   ```powershell
   $url = Get-Content .\endpoint_url.txt
   $body = @{ code = "x = 10`ny = 0`nresult = x / y`nprint(result)" } | ConvertTo-Json
   Invoke-RestMethod -Method POST -Uri $url -ContentType "application/json" -Body $body
   ```

## What This API Does

- Endpoint: `POST /code-interpreter`
- Input:
  ```json
  {"code":"...python code..."}
  ```
- Step 1 (tool function): executes code using `exec()` and captures exact stdout/stderr.
- Step 2:
  - Success: returns `{"error": [], "result": "<exact output>"}`
  - Error: returns traceback in `result` and line number(s) in `error`
- AI analysis:
  - Uses Gemini structured output when `GEMINI_API_KEY` exists.
  - Falls back to traceback line extraction if key is missing/unavailable.
- CORS is enabled for testing.

## Common Errors and Fixes

- `address already in use`:
  ```powershell
  .\stop_all.ps1
  .\start_all.ps1
  ```

- `GEMINI_API_KEY` not found:
  - Set it in the same shell where you run `start_all.ps1`.
  - Without key, fallback line parser is used.

- Cloudflared shows `cert.pem` warning:
  - Normal for quick tunnels. Ignore if `https://...trycloudflare.com` URL appears.

## Files

- `main.py`: FastAPI app (`/code-interpreter`)
- `requirements.txt`: dependencies
- `start_api.ps1`: start API on port `8001`
- `start_tunnel.ps1`: open Cloudflare tunnel
- `start_all.ps1`: start both and print final URL
- `stop_all.ps1`: stop q3 processes

## Final Answer (for grader)

Read from:

`endpoint_url.txt`

Current run endpoint:

`https://untitled-exempt-badly-prime.trycloudflare.com/code-interpreter`
