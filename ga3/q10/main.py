import re
import sys

import fitz  # PyMuPDF


CURRENCY_RE = re.compile(r"\b(\d+(?:\.\d+)?)\s*(Rs|Rupees|Dollar|Dollars|USD)\b", re.I)
DATE_PATTERNS = [
    re.compile(r"\bJanuary\s*0?(\d{1,2})\b", re.I),
    re.compile(r"\b0?(\d{1,2})\s*January\b", re.I),
    re.compile(r"\bJan\s*0?(\d{1,2})\b", re.I),
    re.compile(r"\b0?(\d{1,2})\s*Jan\b", re.I),
]


def parse_target_day(target: str) -> int:
    m = re.search(r"(\d{1,2})", target)
    if not m:
        raise ValueError("Could not parse day from target date")
    day = int(m.group(1))
    if day < 1 or day > 31:
        raise ValueError("Day must be in 1..31")
    return day


def extract_day(line: str):
    for p in DATE_PATTERNS:
        m = p.search(line)
        if m:
            return int(m.group(1))
    return None


def compute_total(pdf_path: str, target_day: int) -> float:
    total_rs = 0.0
    doc = fitz.open(pdf_path)
    try:
        for page in doc:
            for raw in page.get_text("text").splitlines():
                line = raw.strip()
                if not line or line.lower().startswith("expense report"):
                    continue

                day = extract_day(line)
                currency_match = CURRENCY_RE.search(line)
                if day is None or not currency_match:
                    continue

                if day != target_day:
                    continue

                amount = float(currency_match.group(1))
                currency = currency_match.group(2).lower()
                if currency in {"dollar", "dollars", "usd"}:
                    total_rs += amount * 80
                else:
                    total_rs += amount
    finally:
        doc.close()
    return total_rs


def main():
    if len(sys.argv) != 3:
        print("Usage: python main.py <pdf_path> <target_date_like_21Jan>")
        sys.exit(1)

    pdf_path = sys.argv[1]
    target = sys.argv[2]
    target_day = parse_target_day(target)
    total = compute_total(pdf_path, target_day)

    # Print integer if mathematically whole; else print decimal.
    if abs(total - round(total)) < 1e-9:
        print(int(round(total)))
    else:
        print(total)


if __name__ == "__main__":
    main()
