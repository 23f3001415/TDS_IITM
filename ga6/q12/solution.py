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


def preprocess(df, monotone_col):
    """Clip outliers and fill missing values."""
    result = df.copy()
    for col in result.select_dtypes(include="number").columns:
        lo = result[col].quantile(0.1)
        hi = result[col].quantile(0.9)
        result[col] = result[col].clip(lo, hi)
    result = result.fillna(method="ffill").fillna(method="bfill")
    return result


def resolve_input() -> Path:
    here = Path(__file__).resolve().parent
    if len(sys.argv) > 1:
        return Path(sys.argv[1]).resolve()
    return here / "records.csv"


def values_differ(a, b, tol=1e-9) -> bool:
    if pd.isna(a) and pd.isna(b):
        return False
    if pd.isna(a) != pd.isna(b):
        return True
    if isinstance(a, (float, int)) and isinstance(b, (float, int)):
        return abs(float(a) - float(b)) > tol
    return a != b


def main() -> None:
    input_path = resolve_input()
    df = pd.read_csv(input_path)

    result1 = preprocess(df, "value_a")
    result2 = preprocess(result1, "value_a")

    idempotency_violations = 0
    for i in range(len(df)):
        row_bad = any(values_differ(result1.iloc[i][col], result2.iloc[i][col]) for col in df.columns)
        idempotency_violations += int(row_bad)

    monotonicity_violations = 0
    original = df["value_a"]
    processed = result1["value_a"]
    for i in range(len(df)):
        if pd.isna(original.iloc[i]):
            continue
        for j in range(i + 1, len(df)):
            if pd.isna(original.iloc[j]):
                continue
            # Count each pair once. If original value_a[i] > value_a[j],
            # the processed output must preserve that strict ordering.
            if original.iloc[i] > original.iloc[j] and not (processed.iloc[i] > processed.iloc[j]):
                monotonicity_violations += 1

    null_stability_violations = 0
    for i in range(len(df)):
        if df.iloc[i].isna().sum() == 0 and result1.iloc[i].isna().sum() > 0:
            null_stability_violations += 1

    answer = f"{idempotency_violations},{monotonicity_violations},{null_stability_violations}"
    print(answer)


if __name__ == "__main__":
    main()
