# /// script
# requires-python = ">=3.11"
# dependencies = ["sentence-transformers", "numpy"]
# ///

from __future__ import annotations

from pathlib import Path

import numpy as np
from sentence_transformers import SentenceTransformer

HEADLINES = [
    "Open-source language model surpasses proprietary benchmarks on reasoning tasks",
    "Clinical trial shows promising results for Alzheimer's disease treatment",
    "Mental health app demonstrates effectiveness in reducing anxiety symptoms",
    "Hospital introduces AI-assisted imaging system to reduce diagnostic errors",
    "Study links ultra-processed food consumption to increased cardiovascular risk",
    "Gene therapy trial restores vision in patients with inherited retinal disease",
]


def cosine_distance_to_centroid(x: np.ndarray, centroid: np.ndarray) -> np.ndarray:
    x_norm = np.linalg.norm(x, axis=1)
    c_norm = np.linalg.norm(centroid)
    sim = (x @ centroid) / (x_norm * c_norm + 1e-12)
    return 1.0 - sim


def main() -> None:
    model = SentenceTransformer("all-MiniLM-L6-v2")
    emb = np.asarray(model.encode(HEADLINES, convert_to_numpy=True), dtype=np.float64)

    centroid = emb.mean(axis=0)
    distances = cosine_distance_to_centroid(emb, centroid)
    outlier_idx = int(np.argmax(distances))
    outlier_headline = HEADLINES[outlier_idx]

    base_dir = Path(__file__).resolve().parent
    (base_dir / "distances.txt").write_text(
        "\n".join(f"[{i}] {distances[i]:.8f} :: {HEADLINES[i]}" for i in range(len(HEADLINES))) + "\n",
        encoding="utf-8",
    )
    (base_dir / "answer.txt").write_text(f"{outlier_headline}\n", encoding="utf-8")
    print(outlier_headline)


if __name__ == "__main__":
    main()
