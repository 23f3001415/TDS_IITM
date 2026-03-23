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
    input_path = base_dir / "q-wma-regional-sales.csv"

    df = pd.read_csv(input_path)

    east = df[df["Region"].astype(str).str.strip().str.lower() == "east"].copy()
    east = east.sort_values("Week").reset_index(drop=True)
    window = east[east["Week"].between(22, 26)].sort_values("Week")

    weights = np.array([1, 2, 3, 4, 5], dtype=float)
    revenues = window["Revenue"].astype(float).to_numpy()

    if len(revenues) != 5:
        raise RuntimeError("Expected exactly 5 East-region rows for weeks 22..26.")

    wma = float((weights * revenues).sum() / weights.sum())
    answer = f"{wma:.2f}"

    (base_dir / "east_weeks_22_26.csv").write_text(window.to_csv(index=False), encoding="utf-8")
    (base_dir / "answer.txt").write_text(f"{answer}\n", encoding="utf-8")
    print(answer)


if __name__ == "__main__":
    main()

