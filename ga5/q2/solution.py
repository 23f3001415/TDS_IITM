# /// script
# requires-python = ">=3.11"
# dependencies = ["sentence-transformers", "Pillow", "numpy"]
# ///

from __future__ import annotations

from pathlib import Path

import numpy as np
from PIL import Image
from sentence_transformers import SentenceTransformer

TEXT_QUERY = "fall foliage with brown and orange leaves on a park path"


def cosine_similarity_matrix(vec: np.ndarray, mat: np.ndarray) -> np.ndarray:
    vec_norm = np.linalg.norm(vec)
    mat_norm = np.linalg.norm(mat, axis=1)
    return (mat @ vec) / (mat_norm * vec_norm + 1e-12)


def main() -> None:
    base_dir = Path(__file__).resolve().parent
    image_dir = base_dir / "images"
    image_paths = sorted(image_dir.glob("img_*.jpg"))

    if len(image_paths) != 10:
        raise RuntimeError(f"Expected 10 images, found {len(image_paths)} in {image_dir}")

    images = [Image.open(path).convert("RGB") for path in image_paths]

    model = SentenceTransformer("clip-ViT-B-32")
    image_embeddings = np.asarray(model.encode(images, convert_to_numpy=True))
    text_embedding = np.asarray(model.encode(TEXT_QUERY, convert_to_numpy=True))

    scores = cosine_similarity_matrix(text_embedding, image_embeddings)
    best_idx = int(np.argmax(scores))
    best_file = image_paths[best_idx].name

    (base_dir / "answer.txt").write_text(f"{best_file}\n", encoding="utf-8")
    print(best_file)


if __name__ == "__main__":
    main()

