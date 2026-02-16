# Q17 Create a localtunnel Tunnel (ELI15, Complete Beginner)

Think of your laptop as a room inside a locked building.
`localtunnel` gives that room a temporary public door (URL), so anyone on the internet can open your local page.

## Assignment target
- Run a local web server.
- Expose it with `localtunnel`.
- Submit the public URL (`https://something.loca.lt`).
- That URL should show your email: `23f3001415@ds.study.iitm.ac.in`.

## Files used
- `ga2/q17/index.html` -> simple page containing your email
- `ga2/q17/ELI15_q17_solution.md` -> this guide
- `ga2/q17/tunnel_url.txt` -> exact URL to submit

## Step-by-step for a complete novice
1. Open terminal in `ga2/q17`.
2. Start local server on port `5600`:
```bash
python -m http.server 5600
```
3. Open another terminal and create tunnel:
```bash
npx localtunnel --port 5600
```
4. Wait for a line like:
```text
your url is: https://random-name.loca.lt
```
5. Open that URL in browser. You should see your email on the page.
6. Submit that URL in the assignment.

## URL for this run
`https://chatty-news-tie.loca.lt`

## Important gotcha
This URL is temporary. If the terminal stops, the link stops and you need a new URL.
