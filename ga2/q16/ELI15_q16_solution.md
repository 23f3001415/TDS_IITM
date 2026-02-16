# Q16 Public Tunnel with cloudflared (ELI15, Complete Beginner)

Think of your laptop as a house behind a locked gate (NAT/firewall).
`cloudflared` makes a safe outgoing tunnel from your house to Cloudflare, then gives you a public URL so others can visit your local webpage.

## Goal
Create a public URL ending in `.trycloudflare.com` that shows content from your local server running on port `5500`.

## Files for this question
- `ga2/q16/index.html` -> simple page to prove your local server is reachable
- `ga2/q16/ELI15_q16_solution.md` -> this beginner guide

## Step-by-step (novice friendly)
1. Open terminal in `ga2/q16`.
2. Start local web server on port `5500`:
```bash
python -m http.server 5500
```
3. Open another terminal and start quick tunnel:
```bash
cloudflared tunnel --url http://localhost:5500
```
4. Wait for output showing a URL like:
```text
https://random-words.trycloudflare.com
```
5. Open that URL in a browser. If you see your `index.html` content, done.
6. Submit that full URL in the assignment.

## Public URL for this run
`https://americas-final-certainly-saw.trycloudflare.com`

## Important gotcha
Quick tunnel URLs are temporary. If you stop `cloudflared` (or reboot), you get a new URL next time.
