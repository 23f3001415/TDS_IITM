# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "numpy",
#   "openai",
#   "scikit-learn",
# ]
# ///

from __future__ import annotations

import os
import sys
from pathlib import Path

import numpy as np
from openai import OpenAI
from sklearn.cluster import KMeans


def load_dotenv_if_present() -> None:
    env_path = Path(__file__).resolve().parent / ".env"
    if not env_path.exists():
        return

    for raw in env_path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and value and key not in os.environ:
            os.environ[key] = value


def resolve_input_path() -> Path:
    if len(sys.argv) > 1:
        return Path(sys.argv[1]).expanduser().resolve()

    here = Path(__file__).resolve().parent
    candidates = [
        here / "q-embeddings-clustering.txt",
        here / "product_descriptions.txt",
    ]
    for candidate in candidates:
        if candidate.exists():
            return candidate

    raise FileNotFoundError(
        "Input file not found. Put q-embeddings-clustering.txt next to solution.py "
        "or pass its path: uv run solution.py <path-to-file>"
    )


def resolve_client() -> OpenAI:
    api_key = (
        os.getenv("OPENAI_API_KEY")
        or os.getenv("AIPIPE_TOKEN")
        or os.getenv("AIPROXY_TOKEN")
    )
    if not api_key:
        raise RuntimeError(
            "Missing API key. Set OPENAI_API_KEY (or AIPIPE_TOKEN/AIPROXY_TOKEN)."
        )

    base_url = os.getenv("OPENAI_BASE_URL")
    if not base_url and (os.getenv("AIPIPE_TOKEN") or os.getenv("AIPROXY_TOKEN")):
        base_url = "https://aipipe.org/openai/v1"

    if base_url:
        return OpenAI(api_key=api_key, base_url=base_url)
    return OpenAI(api_key=api_key)


def main() -> None:
    load_dotenv_if_present()

    input_path = resolve_input_path()
    descriptions = [line.strip() for line in input_path.read_text(encoding="utf-8").splitlines() if line.strip()]

    if not descriptions:
        raise RuntimeError("Input file has no non-empty descriptions.")

    client = resolve_client()
    response = client.embeddings.create(
        model="text-embedding-3-small",
        input=descriptions,
    )
    embeddings = np.array([item.embedding for item in response.data], dtype=np.float32)

    model = KMeans(n_clusters=5, random_state=42, n_init=10)
    labels = model.fit_predict(embeddings)

    unique, counts = np.unique(labels, return_counts=True)
    max_index = int(np.argmax(counts))
    cluster_label = int(unique[max_index])
    count = int(counts[max_index])

    answer = f"{cluster_label}, {count}"
    (input_path.parent / "answer.txt").write_text(f"{answer}\n", encoding="utf-8")
    print(answer)


if __name__ == "__main__":
    main()
