# Q17: Extract Structured Data with Schema Validation

## ELI15 Step-by-Step

1. Keep the sample clinical-trial text as input.
2. Define a JSON schema:
   - Required: `trialId`, `phase`, `participants`, `intervention`
   - Optional: `outcomes`, `status`
3. Call AI Pipe (`https://aipipe.org/openai/v1/chat/completions`) with `response_format={"type":"json_object"}`.
4. Parse the JSON returned by the model.
5. Validate required fields, data types, and format quality checks.
6. If validation fails, retry with error feedback (max 3 tries).
7. If API/retries fail, use regex fallback extraction.
8. Return final JSON with:
   - `schema`
   - `extracted`
   - `validated`
   - `confidence`
   - `errors`
   - `retryCount`
   - `model`

## Run

```powershell
cd ga3/q17
$env:AIPIPE_TOKEN="your_token_here"
python main.py
```

## Submission

Paste the JSON printed by `main.py`.
