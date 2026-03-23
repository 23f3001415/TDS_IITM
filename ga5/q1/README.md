# Q1: Embeddings - K-Means Clustering on Product Descriptions

## ELI15 Step-by-Step (Complete Beginner)

1. Think of each product description as a sentence we must convert into numbers.
2. We use OpenAI model `text-embedding-3-small` to convert each sentence into a long number-list (an embedding vector).
3. Similar products get similar vectors, so products that "mean" similar things end up closer together.
4. We run K-Means clustering with exactly 5 clusters (`k=5`), using:
   `KMeans(n_clusters=5, random_state=42, n_init=10)`.
5. K-Means gives every product a label from `0` to `4`.
6. We count how many products are in each label.
7. We pick the label with the biggest count.
8. We submit in this exact format: `cluster_label, count` (example: `2, 14`).

## Files in This Folder

- `q-embeddings-clustering.txt`: your 50 descriptions
- `solution.py`: computes the final answer
- `answer.txt`: auto-created after run

## Run Commands (PowerShell)

```powershell
cd C:\Users\sriva\OneDrive\Documents\TDS\ga5\q1

# Use one of these key options:
# Option A: OpenAI key
$env:OPENAI_API_KEY="your_key_here"

# Option B: AI Pipe token (if you use aipipe)
# $env:AIPIPE_TOKEN="your_token_here"
# $env:OPENAI_BASE_URL="https://aipipe.org/openai/v1"

uv run solution.py
```

Optional shortcut:

1. Create `ga5/q1/.env`
2. Put one of these:
   - `OPENAI_API_KEY=...`
   - `AIPIPE_TOKEN=...`
3. Run `uv run solution.py` (script auto-loads `.env`)

## What You Submit

- The terminal prints the final answer as:
  `cluster_label, count`
- The same value is also saved in `answer.txt`.

Submit that exact text to the grader.
