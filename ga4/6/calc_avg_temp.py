import json
from datetime import datetime


FILE_PATH = r"C:\Users\sriva\Downloads\q-json-sensor-rollup.jsonl"
START_TS = datetime.fromisoformat("2024-07-05T17:22:24.618+00:00")
END_TS = datetime.fromisoformat("2024-07-10T17:22:24.618+00:00")


def to_celsius(value, unit):
    unit = str(unit).strip().upper()
    if unit == "C":
        return float(value)
    if unit == "F":
        return (float(value) - 32.0) * (5.0 / 9.0)
    return None


def main():
    total_c = 0.0
    count = 0

    with open(FILE_PATH, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue

            row = json.loads(line)

            site = str(row.get("site", "")).strip()
            device = str(row.get("device", "")).strip().lower()
            status = str(row.get("status", "")).strip().lower()
            captured_at = str(row.get("captured_at", "")).strip()

            if site != "Plant-02":
                continue
            if not device.startswith("condenser"):
                continue
            if status in {"maintenance", "offline"}:
                continue
            if not captured_at:
                continue

            try:
                dt = datetime.fromisoformat(captured_at.replace("Z", "+00:00"))
            except ValueError:
                continue

            if not (START_TS <= dt <= END_TS):
                continue

            temp = ((row.get("metrics") or {}).get("temperature") or {})
            value = temp.get("value")
            unit = temp.get("unit")
            if value is None:
                continue

            celsius = to_celsius(value, unit)
            if celsius is None:
                continue

            total_c += celsius
            count += 1

    avg_c = round(total_c / count, 2) if count else None
    print(avg_c)


if __name__ == "__main__":
    main()
