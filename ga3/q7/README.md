# Q7: LLM Audio Processing - YouTube Topic Timestamp Finder

## ELI15 Step-by-Step (Beginner Friendly)

1. Open PowerShell in `ga3/q7`.
2. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```
3. Set Gemini key in same terminal (recommended):
   ```powershell
   $env:GEMINI_API_KEY="your_gemini_api_key_here"
   ```
4. Start API + tunnel:
   ```powershell
   .\start_all.ps1
   ```
5. It prints a base URL like:
   `https://something.trycloudflare.com`
6. Submit that base URL (grader will call `/ask` automatically).
7. Test manually:
   ```powershell
   $base = Get-Content .\base_url.txt
   $body = @{
     video_url = "https://youtu.be/dQw4w9WgXcQ"
     topic = "never gonna give you up"
   } | ConvertTo-Json
   Invoke-RestMethod -Uri "$base/ask" -Method POST -ContentType "application/json" -Body $body
   ```

## What This API Does

- Endpoint: `POST /ask`
- Input:
  ```json
  {"video_url":"...","topic":"..."}
  ```
- Uses `yt-dlp` to download audio-only from YouTube.
- Uploads audio via Gemini Files API when `GEMINI_API_KEY` is available.
- Polls upload state until file becomes `ACTIVE`.
- Requests structured JSON output with `timestamp` in `HH:MM:SS`.
- Also downloads subtitles and uses phrase matching as a fallback.
- Cleans temporary files automatically using `TemporaryDirectory`.
- Returns:
  ```json
  {"timestamp":"HH:MM:SS","video_url":"...","topic":"..."}
  ```

## Files

- `main.py`: FastAPI app with `/ask`
- `requirements.txt`: dependencies
- `start_api.ps1`: start API on port `8002`
- `start_tunnel.ps1`: start Cloudflare tunnel
- `start_all.ps1`: start both and print base URL
- `stop_all.ps1`: stop q7 processes
- `base_url.txt`: live submit URL for current run

## Final Answer (for grader)

Read from:

`base_url.txt`

Current run base URL:

`https://gym-exterior-males-dept.trycloudflare.com`
