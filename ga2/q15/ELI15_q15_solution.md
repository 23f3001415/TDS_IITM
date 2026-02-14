# Q15 - Cloudflare Workers Serverless Deployment (ELI15 Guide)

Think of a Cloudflare Worker like a tiny program that runs near users worldwide.
For this question, your Worker receives JSON, reverses data based on type, and returns your IITM email.

## What the endpoint must do
- Route: `POST /data`
- Input JSON: `{ "type": "...", "value": ... }`
- Output JSON: `{ "reversed": ..., "email": "23f3001415@ds.study.iitm.ac.in" }`
- Must support:
  - `string`: reverse characters
  - `array`: reverse element order
  - `words`: reverse word order
  - `number`: reverse digits and return integer
- CORS: allow cross-origin POST requests

## Files created
- `ga2/q15/src/worker.js`
- `ga2/q15/wrangler.toml`
- `ga2/q15/package.json`

## Step-by-step (beginner)
1. Open terminal in `ga2/q15`.
2. Login once:

```bash
npx wrangler login
```

3. Deploy:

```bash
npx wrangler deploy
```

4. Wrangler prints a URL like:

```text
https://ga2-q15-23f3001415.<subdomain>.workers.dev
```

5. Your final endpoint to submit is that URL + `/data`.

## Test command
Use this to verify grader payload behavior:

```bash
curl -X POST "https://<your-worker-url>/data" \
  -H "Content-Type: application/json" \
  -d '{"type":"number","value":67041}'
```

Expected `reversed` for grader payload: `14076`

## Final submission format
`https://<your-worker-url>/data`
