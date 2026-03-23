# /// script
# requires-python = ">=3.11"
# dependencies = ["pandas"]
# ///

from __future__ import annotations

from pathlib import Path

import pandas as pd


def main() -> None:
    base_dir = Path(__file__).resolve().parent
    input_path = base_dir / "server_access_logs.csv"
    df = pd.read_csv(input_path)

    # Step A: scraper IP based on 429 responses on /api/pricing
    rate_limited = df[(df["status_code"] == 429) & (df["endpoint"] == "/api/pricing")]
    scraper_ip = rate_limited["ip_address"].value_counts().idxmax()

    # Step B: median response time across ALL rows for scraper IP
    scraper_rows = df[df["ip_address"] == scraper_ip]
    median_rt = float(scraper_rows["response_time_ms"].median())

    answer = f"{scraper_ip}, {median_rt:.1f}"
    (base_dir / "answer.txt").write_text(f"{answer}\n", encoding="utf-8")
    print(answer)


if __name__ == "__main__":
    main()

