# Q15 Cloudflare Worker (ELI15, Complete Beginner)

Imagine a Cloudflare Worker as a tiny robot on the internet.  
You send it data, it changes the data, and sends the result back very fast.

For this assignment, your robot must listen at `POST /data` and return:

```json
{ "reversed": ..., "email": "23f3001415@ds.study.iitm.ac.in" }
```

## 1. What this Worker does
- Accepts JSON: `{ "type": "...", "value": ... }`
- Supports:
  - `string`: reverse characters
  - `array`: reverse array order
  - `words`: reverse word order in a sentence
  - `number`: reverse digits and return an integer
- Handles CORS for cross-origin `POST` (and `OPTIONS` preflight)

## 2. Files in this solution
- `ga2/q15/src/worker.js` -> Worker logic and routing
- `ga2/q15/wrangler.toml` -> Cloudflare deployment config
- `ga2/q15/package.json` -> project metadata/scripts

## 3. Step-by-step to understand and reproduce
1. Open terminal in `ga2/q15`.
2. Install dependencies once:
```bash
npm install
```
3. Log in to Cloudflare (first time only):
```bash
npx wrangler login
```
4. Deploy:
```bash
npx wrangler deploy
```
5. Submit the URL with `/data` at the end.

## 4. Deployed endpoint for this submission
`https://ga2-q15-23f3001415.tds-23f3001415.workers.dev/data`

## 5. Grader payload test
If grader sends:

```json
{"type":"number","value":67041}
```

Expected:

```json
{"reversed":14076,"email":"23f3001415@ds.study.iitm.ac.in"}
```

## 6. Quick manual tests
```bash
curl -X POST "https://ga2-q15-23f3001415.tds-23f3001415.workers.dev/data" -H "Content-Type: application/json" -d "{\"type\":\"string\",\"value\":\"hello\"}"
curl -X POST "https://ga2-q15-23f3001415.tds-23f3001415.workers.dev/data" -H "Content-Type: application/json" -d "{\"type\":\"array\",\"value\":[1,2,3]}"
curl -X POST "https://ga2-q15-23f3001415.tds-23f3001415.workers.dev/data" -H "Content-Type: application/json" -d "{\"type\":\"words\",\"value\":\"cloudflare worker test\"}"
curl -X POST "https://ga2-q15-23f3001415.tds-23f3001415.workers.dev/data" -H "Content-Type: application/json" -d "{\"type\":\"number\",\"value\":67041}"
```
