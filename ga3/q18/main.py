import argparse
import re
from pathlib import Path

import pandas as pd


COUNTRY_MAP = {
    "US": "US",
    "USA": "US",
    "U.S.A": "US",
    "UNITED STATES": "US",
    "UK": "UK",
    "U.K": "UK",
    "UNITED KINGDOM": "UK",
    "FR": "FR",
    "FRA": "FR",
    "FRANCE": "FR",
    "BR": "BR",
    "BRA": "BR",
    "BRAZIL": "BR",
    "IN": "IN",
    "IND": "IN",
    "INDIA": "IN",
    "AE": "AE",
    "UAE": "AE",
    "U.A.E": "AE",
    "UNITED ARAB EMIRATES": "AE",
}


def normalize_country(value: object) -> str:
    text = str(value).strip().upper().replace(".", "")
    return COUNTRY_MAP.get(text, text)


def parse_date(value: object) -> pd.Timestamp:
    text = str(value).strip()
    if "-" in text:
        return pd.to_datetime(text, format="%m-%d-%Y", errors="coerce")
    return pd.to_datetime(text, format="%Y/%m/%d", errors="coerce")


def parse_money(value: object) -> float | None:
    if pd.isna(value):
        return None
    text = str(value).replace("USD", "").strip()
    text = re.sub(r"\s+", "", text)
    if not text:
        return None
    return float(text)


def calculate_margin(excel_path: Path) -> tuple[float, float, float]:
    df = pd.read_excel(excel_path)

    df["country_clean"] = df["Country"].map(normalize_country)
    df["date_clean"] = df["Date"].map(parse_date)
    df["product_clean"] = df["Product/Code"].astype(str).str.split("/").str[0].str.strip()
    df["sales_clean"] = df["Sales"].map(parse_money)
    df["cost_clean"] = df["Cost"].map(parse_money)
    df["cost_clean"] = df["cost_clean"].fillna(df["sales_clean"] * 0.5)

    cutoff = pd.Timestamp("2022-08-25 14:57:47")
    mask = (
        (df["date_clean"] <= cutoff)
        & (df["product_clean"].str.upper() == "ALPHA")
        & (df["country_clean"] == "UK")
    )
    filtered = df[mask]

    total_sales = float(filtered["sales_clean"].sum())
    total_cost = float(filtered["cost_clean"].sum())
    margin = (total_sales - total_cost) / total_sales
    return total_sales, total_cost, margin


def main() -> None:
    parser = argparse.ArgumentParser(description="Clean Excel sales data and compute margin.")
    parser.add_argument(
        "excel_file",
        nargs="?",
        default=r"C:\Users\sriva\Downloads\q-clean-up-excel-sales-data.xlsx",
        help="Path to q-clean-up-excel-sales-data.xlsx",
    )
    args = parser.parse_args()

    excel_path = Path(args.excel_file)
    sales, cost, margin = calculate_margin(excel_path)
    print(f"TOTAL_SALES={sales:.2f}")
    print(f"TOTAL_COST={cost:.2f}")
    print(f"MARGIN_DECIMAL={margin:.12f}")
    print(f"MARGIN_PERCENT={margin*100:.6f}%")


if __name__ == "__main__":
    main()
