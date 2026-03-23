# /// script
# requires-python = ">=3.11"
# ///

from __future__ import annotations

import csv
import re
import sys
from pathlib import Path


def tokenize(text: str) -> list[str]:
    return [w for w in re.sub(r"[^a-z0-9\s]", " ", text.lower()).split() if w]


def ngrams(tokens: list[str], n: int = 8) -> set[str]:
    if len(tokens) < n:
        return set()
    return {" ".join(tokens[i : i + n]) for i in range(len(tokens) - n + 1)}


def overlap_score(question: str, corpus_ngrams: set[str], n: int = 8) -> float:
    qg = ngrams(tokenize(question), n)
    if not qg:
        return 0.0
    hits = sum(1 for gram in qg if gram in corpus_ngrams)
    return hits / len(qg)


def resolve_paths() -> tuple[Path, Path]:
    here = Path(__file__).resolve().parent
    if len(sys.argv) >= 3:
        return Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
    return here / "questions.csv", here / "corpus.txt"


def main() -> None:
    questions_path, corpus_path = resolve_paths()

    corpus_text = corpus_path.read_text(encoding="utf-8")
    corpus_ngrams = ngrams(tokenize(corpus_text), 8)

    with questions_path.open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f))

    contaminated_count = 0
    total_correct = 0
    clean_correct = 0
    clean_count = 0

    for row in rows:
        score = overlap_score(row["question"], corpus_ngrams, 8)
        contaminated = score > 0.5
        correct = int(row["is_correct"])

        contaminated_count += int(contaminated)
        total_correct += correct

        if not contaminated:
            clean_count += 1
            clean_correct += correct

    reported_accuracy = round(total_correct / len(rows) * 100, 2)
    adjusted_accuracy = round(clean_correct / clean_count * 100, 2)

    answer = f"{contaminated_count},{reported_accuracy:.2f},{adjusted_accuracy:.2f}"
    print(answer)


if __name__ == "__main__":
    main()
