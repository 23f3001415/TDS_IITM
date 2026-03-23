# /// script
# requires-python = ">=3.11"
# dependencies = ["pandas"]
# ///

from __future__ import annotations

from itertools import combinations
from pathlib import Path

import pandas as pd

COLUMNS = [
    "Study_Hours",
    "Sleep_Hours",
    "Screen_Time",
    "Attendance_Percent",
    "Exam_Score",
]


def main() -> None:
    base_dir = Path(__file__).resolve().parent
    input_path = base_dir / "q-correlation-excel.csv"
    df = pd.read_csv(input_path)

    corr = df[COLUMNS].corr(method="pearson")

    best_pair = None
    best_value = float("-inf")
    for a, b in combinations(COLUMNS, 2):
        value = float(corr.loc[a, b])
        if value > best_value:
            best_value = value
            best_pair = (a, b)

    assert best_pair is not None
    answer = f"{best_pair[0]}, {best_pair[1]}, {best_value:.4f}"

    (base_dir / "answer.txt").write_text(f"{answer}\n", encoding="utf-8")
    print(answer)


if __name__ == "__main__":
    main()

