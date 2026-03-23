# Q3: LLM Topic Modeling - News Headlines Classification

## ELI15 Step-by-Step (Complete Beginner)

1. You got a CSV with 200 headlines in one column called `headline`.
2. For each headline, we must pick exactly one topic from:
   `Politics, Sports, Technology, Business, Entertainment`.
3. We use an LLM (`gpt-4o-mini`) as a classifier with `temperature=0` so output is stable.
4. To save time and money, we classify 10 headlines in one API call (batching).
5. The model must return JSON labels in order; script checks labels are valid.
6. If a batch response is malformed, script retries and falls back to single-headline classification.
7. After all 200 are labeled, we count how many are `Technology`.
8. Submit only that integer.

## Files in This Folder

- `q-topic-modeling-llm.csv`: input file with 200 headlines
- `solution.py`: batch classifier script
- `classified_headlines.csv`: output with `headline,topic` (auto-created)
- `answer.txt`: final Technology count (auto-created)

## Run

```powershell
cd C:\Users\sriva\OneDrive\Documents\TDS\ga5\q3

# Option 1: AI Pipe
$env:AIPIPE_TOKEN="your_token_here"
$env:OPENAI_BASE_URL="https://aipipe.org/openai/v1"

# Option 2: OpenAI direct
# $env:OPENAI_API_KEY="your_key_here"

uv run solution.py
```

You can also place credentials in `ga5/q3/.env`:

```env
AIPIPE_TOKEN=...
OPENAI_BASE_URL=https://aipipe.org/openai/v1
```

## Submission

Submit the single integer printed as the Technology count.

