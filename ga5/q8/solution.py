# /// script
# requires-python = ">=3.11"
# dependencies = ["pandas"]
# ///

from __future__ import annotations

from pathlib import Path

import pandas as pd


def main() -> None:
    base_dir = Path(__file__).resolve().parent
    input_path = base_dir / "q-stock-prices-ema.csv"

    df = pd.read_csv(input_path)
    df["Date"] = pd.to_datetime(df["Date"])
    df = df.sort_values(["Ticker", "Date"]).reset_index(drop=True)

    df["EMA_21"] = df.groupby("Ticker")["Close_Price"].transform(
        lambda x: x.ewm(span=21, adjust=False).mean()
    )

    last_date = df["Date"].max()
    last_day = df[df["Date"] == last_date]

    winner_row = last_day.loc[last_day["EMA_21"].idxmax()]
    winner_ticker = str(winner_row["Ticker"]).upper()
    winner_ema = float(winner_row["EMA_21"])

    answer = f"{winner_ema:.2f}, {winner_ticker}"
    (base_dir / "answer.txt").write_text(f"{answer}\n", encoding="utf-8")
    print(answer)


if __name__ == "__main__":
    main()

