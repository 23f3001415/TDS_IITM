import re


FILE_PATH = r"C:\Users\sriva\Downloads\q-parse-partial-json.jsonl"
SALES_PATTERN = re.compile(r'"sales"\s*:\s*(-?\d+(?:\.\d+)?)')


def main():
    total = 0.0
    rows = 0
    recovered = 0

    with open(FILE_PATH, "r", encoding="utf-8") as f:
        for line in f:
            rows += 1
            match = SALES_PATTERN.search(line)
            if not match:
                continue

            total += float(match.group(1))
            recovered += 1

    # Print int if whole number, otherwise keep decimal.
    if total.is_integer():
        print(int(total))
    else:
        print(total)

    # Optional debug info:
    # print(f"rows={rows}, recovered={recovered}")


if __name__ == "__main__":
    main()
