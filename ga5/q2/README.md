# Q2: Multimodal Embeddings - CLIP Image Search

## ELI15 Step-by-Step (Complete Beginner)

1. You have 10 images and 1 text sentence (your query).
2. We use a CLIP model (`clip-ViT-B-32`) that can turn both text and images into vectors in the same space.
3. For each image, we compare its vector with the text vector using cosine similarity.
4. Cosine similarity tells us how close two vectors point in the same direction.
5. The image with the highest cosine score is the best match.
6. We print only the filename like `img_07.jpg` (this is what the grader wants).

## Files in This Folder

- `q-multimodal-image-search.zip`: downloaded ZIP
- `images/img_01.jpg` ... `images/img_10.jpg`: extracted images
- `solution.py`: CLIP + cosine similarity solver
- `answer.txt`: auto-written final filename after running

## Run

```powershell
cd C:\Users\sriva\OneDrive\Documents\TDS\ga5\q2
uv run solution.py
```

## Submission Format

Submit just the filename:

```text
img_07.jpg
```

