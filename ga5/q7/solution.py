# /// script
# requires-python = ">=3.11"
# dependencies = ["pandas"]
# ///

from __future__ import annotations

from pathlib import Path

import pandas as pd


def main() -> None:
    base_dir = Path(__file__).resolve().parent
    input_path = base_dir / "q-outlier-detection-excel.csv"

    df = pd.read_csv(input_path)
    values = df["Delivery_Minutes"].astype(float)

    mean = values.mean()
    std_sample = values.std(ddof=1)  # Excel STDEV (sample standard deviation)
    z_scores = (values - mean) / std_sample

    outlier_count = int((z_scores.abs() > 2).sum())

    (base_dir / "answer.txt").write_text(f"{outlier_count}\n", encoding="utf-8")
    print(outlier_count)


if __name__ == "__main__":
    main()

