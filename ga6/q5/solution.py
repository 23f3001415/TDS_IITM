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


def resolve_paths() -> tuple[Path, Path]:
    here = Path(__file__).resolve().parent
    if len(sys.argv) >= 3:
        return Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
    return here / "day1.csv", here / "day2.csv"


def main() -> None:
    day1_path, day2_path = resolve_paths()
    day1 = pd.read_csv(day1_path)
    day2 = pd.read_csv(day2_path)

    bad_rows: set[int] = set()
    today = pd.Timestamp.today().normalize()

    for col in day1.columns:
        s1 = day1[col]
        s2 = day2[col]

        # Rule 1: if Day 1 had no nulls, any Day 2 null is anomalous.
        if s1.isna().sum() == 0:
            bad_rows.update(s2[s2.isna()].index.tolist())

        numeric1 = pd.to_numeric(s1, errors="coerce")
        if numeric1.notna().mean() > 0.95:
            numeric2 = pd.to_numeric(s2, errors="coerce")
            low, high = numeric1.min(), numeric1.max()
            mask = (numeric2 < low) | (numeric2 > high)
            bad_rows.update(s2[mask].index.tolist())
            continue

        date1 = pd.to_datetime(s1, errors="coerce", format="mixed")
        if date1.notna().mean() > 0.90:
            date2 = pd.to_datetime(s2, errors="coerce", format="mixed")
            bad_rows.update(s2[date2 > today].index.tolist())
            continue

        if s1.nunique(dropna=True) <= 20:
            allowed = set(s1.dropna())
            mask = ~s2.isna() & ~s2.isin(allowed)
            bad_rows.update(s2[mask].index.tolist())

    print(len(bad_rows))


if __name__ == "__main__":
    main()
