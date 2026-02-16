# Q20 Local Ollama Endpoint (ELI15, Complete Beginner)

Think of Ollama as a local AI server running on your own laptop at `http://localhost:11434`.
For this assignment, we make it reachable from the internet using `ngrok`, and attach your email in response headers.

## Goal
Get a public HTTPS ngrok URL that forwards to local Ollama and returns:
- CORS header: `Access-Control-Allow-Origin`
- Email header: `X-Email` (and `X-User-Email`)
- Valid Ollama JSON response

## Files in this solution
- `ga2/q20/start_ollama.cmd` -> starts Ollama with required env vars
- `ga2/q20/start_ngrok.cmd` -> starts ngrok with response headers
- `ga2/q20/ELI15_q20_solution.md` -> this guide
- `ga2/q20/forwarding_url.txt` -> final URL to submit

## Step-by-step (novice friendly)
1. Install Ollama (one time):
```bash
winget install -e --id Ollama.Ollama
```
2. Start Ollama with CORS enabled:
```bash
start_ollama.cmd
```
This script sets:
- `OLLAMA_ORIGINS=*`
- `OLLAMA_HOST=0.0.0.0:11434`

3. In another terminal, start ngrok:
```bash
start_ngrok.cmd
```
This forwards port `11434` and adds headers:
- `X-Email: 23f3001415@ds.study.iitm.ac.in`
- `X-User-Email: 23f3001415@ds.study.iitm.ac.in`
- `Access-Control-Expose-Headers: *`
- `Access-Control-Allow-Origin: *`
- `Access-Control-Allow-Headers: *`

4. Copy the ngrok HTTPS forwarding URL.

5. Verify:
```bash
curl "https://<your-ngrok-url>/api/tags" -H "ngrok-skip-browser-warning: true"
```
You should see JSON like:
```json
{"models":[]}
```

## Verified output for this run
- Status: `200`
- `Access-Control-Allow-Origin`: `*, *`
- `X-Email`: `23f3001415@ds.study.iitm.ac.in`
- `X-User-Email`: `23f3001415@ds.study.iitm.ac.in`
- Body: valid Ollama JSON (`{"models":[]}`)

## Final URL to submit
`https://obdurately-ichthyographic-zoraida.ngrok-free.dev`
