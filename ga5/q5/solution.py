# /// script
# requires-python = ">=3.11"
# dependencies = ["pandas", "numpy"]
# ///

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


def main() -> None:
    base_dir = Path(__file__).resolve().parent
    input_path = base_dir / "q-regression-excel.csv"

    df = pd.read_csv(input_path)

    x = df[
        ["Area_SqFt", "Bedrooms", "Age_Years", "Distance_City_Center_Km"]
    ].to_numpy(dtype=float)
    y = df["Price"].to_numpy(dtype=float)

    # OLS with intercept, equivalent to Excel ToolPak Regression.
    x_design = np.column_stack([np.ones(len(x)), x])
    beta, *_ = np.linalg.lstsq(x_design, y, rcond=None)

    x_new = np.array([1.0, 1800.0, 3.0, 10.0, 5.0])
    predicted_price = float(x_new @ beta)

    answer = f"{predicted_price:.2f}"
    (base_dir / "answer.txt").write_text(f"{answer}\n", encoding="utf-8")
    print(answer)


if __name__ == "__main__":
    main()

