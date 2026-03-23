# Q9: The Embedding Auditor

## ELI15 Step-by-Step (Complete Beginner)

1. You have a JSON file containing 40 sentence pairs.
2. Each pair has:
   - a type (`paraphrase`, `negation`, or `near_duplicate`)
   - two embedding vectors
   - a threshold
   - a threshold direction (`>=` or `<=`)
3. Normally cosine similarity is:
   - `(A dot B) / (|A| * |B|)`
4. But the question tells us the vectors are already L2-normalised.
5. That means `|A| = 1` and `|B| = 1`.
6. So cosine similarity becomes just the dot product.
7. Dot product means:
   - multiply matching positions
   - add all the products
8. For each pair:
   - compute `sim = dot(embedding_a, embedding_b)`
9. Then check failure using `threshold_op`:
   - if `threshold_op` is `>=`, the pair fails when `sim < threshold`
   - otherwise, the pair fails when `sim > threshold`
10. Count failures separately for:
   - `paraphrase`
   - `negation`
   - `near_duplicate`
11. Do **not** count total failures only.
12. The grader wants exactly three comma-separated integers in this order:
   - `paraphrase_failures,negation_failures,near_duplicate_failures`
13. Running the audit on your downloaded file gives:
   - `paraphrase = 14`
   - `negation = 0`
   - `near_duplicate = 1`

## Files in This Folder

- `embeddings.json`: copied from your Downloads folder
- `solution.py`: computes the failure counts
- `answer.txt`: final submission string

## Run

```powershell
cd C:\Users\sriva\OneDrive\Documents\TDS\ga6\q9
python solution.py
```

## Final Answer To Submit

```text
14,0,1
```
