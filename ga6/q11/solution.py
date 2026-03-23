# /// script
# requires-python = ">=3.11"
# dependencies = [
#   "pandas",
# ]
# ///

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd


FEATURES = ["age", "income", "education", "hours_per_week"]
REPORTED_ACCURACY = 76.5


def resolve_paths() -> tuple[Path, Path]:
    here = Path(__file__).resolve().parent
    if len(sys.argv) >= 3:
        return Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
    return here / "train.csv", here / "test.csv"


def main() -> None:
    train_path, test_path = resolve_paths()
    train = pd.read_csv(train_path)
    test = pd.read_csv(test_path)

    merged = test.merge(
        train[FEATURES].drop_duplicates(),
        on=FEATURES,
        how="left",
        indicator=True,
    )

    leaked_mask = merged["_merge"] == "both"
    leaked_rows = merged[leaked_mask]
    clean_rows = merged[~leaked_mask]

    leaked_count = int(leaked_mask.sum())
    leaked_accuracy = leaked_rows["is_correct"].mean() * 100
    clean_accuracy = clean_rows["is_correct"].mean() * 100
    inflation_pp = REPORTED_ACCURACY - clean_accuracy

    answer = f"{leaked_count},{leaked_accuracy:.2f},{clean_accuracy:.2f},{inflation_pp:.2f}"
    print(answer)


if __name__ == "__main__":
    main()
