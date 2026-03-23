# /// script
# requires-python = ">=3.11"
# ///

from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path


def dot(a: list[float], b: list[float]) -> float:
    return sum(x * y for x, y in zip(a, b))


def resolve_input() -> Path:
    here = Path(__file__).resolve().parent
    if len(sys.argv) > 1:
        return Path(sys.argv[1]).resolve()
    return here / "embeddings.json"


def main() -> None:
    input_path = resolve_input()
    data = json.loads(input_path.read_text(encoding="utf-8"))

    counts = Counter({"paraphrase": 0, "negation": 0, "near_duplicate": 0})
    for pair in data:
        sim = dot(pair["embedding_a"], pair["embedding_b"])
        fails = sim < pair["threshold"] if pair["threshold_op"] == ">=" else sim > pair["threshold"]
        if fails:
            counts[pair["type"]] += 1

    answer = f"{counts['paraphrase']},{counts['negation']},{counts['near_duplicate']}"
    print(answer)


if __name__ == "__main__":
    main()
