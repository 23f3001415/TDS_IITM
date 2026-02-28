import json
from datetime import datetime, date


FILE_PATH = r"C:\Users\sriva\Downloads\q-json-customer-flatten.jsonl"
START_DATE = date.fromisoformat("2024-04-27")
END_DATE = date.fromisoformat("2024-06-01")


def in_window(order_date_str):
    dt = datetime.fromisoformat(str(order_date_str).replace("Z", "+00:00"))
    d = dt.date()
    return START_DATE <= d <= END_DATE


def main():
    total_quantity = 0

    with open(FILE_PATH, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue

            record = json.loads(line)
            if record.get("region") != "Asia Pacific":
                continue

            for order in (record.get("orders") or []):
                order_date = order.get("order_date")
                if not order_date:
                    continue
                try:
                    if not in_window(order_date):
                        continue
                except ValueError:
                    continue

                for item in (order.get("items") or []):
                    if item.get("category") != "Collaboration":
                        continue

                    # Channel exists at both order and item level; use item and fall back to order.
                    channel = item.get("channel") or order.get("channel")
                    if channel != "Reseller":
                        continue

                    try:
                        total_quantity += int(item.get("quantity"))
                    except (TypeError, ValueError):
                        continue

    print(total_quantity)


if __name__ == "__main__":
    main()
