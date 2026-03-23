# Q13: Embeddings - Semantic Outlier Detection

## ELI15 Step-by-Step (Complete Beginner)

1. Put all 6 headlines in a Python list.
2. Use an embedding model (`all-MiniLM-L6-v2`) to convert each headline into a vector.
3. Compute the centroid (average vector) of all 6 embeddings.
4. For each headline embedding, calculate cosine distance from that centroid.
5. The headline with the largest distance is the semantic outlier.
6. Print and submit the full headline text.

## Files in This Folder

- `solution.py`: embeddings + centroid + cosine-distance outlier detection
- `answer.txt`: final outlier headline text
- `distances.txt`: per-headline cosine distances (for verification)

## Run

```powershell
cd C:\Users\sriva\OneDrive\Documents\TDS\ga5\q13
uv run solution.py
```
