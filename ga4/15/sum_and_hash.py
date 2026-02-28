import hashlib
import json
import zipfile


ZIP_PATH = r"C:\Users\sriva\Downloads\corrupted_logs.zip"
LOG_NAME = "corrupted_logs.json"


def metric_2900_sum_from_valid_lines():
    total = 0

    with zipfile.ZipFile(ZIP_PATH) as zf:
        with zf.open(LOG_NAME) as f:
            for raw in f:
                line = raw.decode("utf-8", errors="replace").strip()
                if not line:
                    continue
                try:
                    record = json.loads(line)
                except json.JSONDecodeError:
                    # Corrupted line: ignore completely.
                    continue

                # Safely extract deeply nested metric_2900 only from valid JSON.
                try:
                    value = record["context"]["system"]["process"]["metrics"]["metric_2900"]
                except (KeyError, TypeError):
                    continue

                if isinstance(value, int) and not isinstance(value, bool):
                    total += value

    return total


def main():
    total = metric_2900_sum_from_valid_lines()
    digest = hashlib.sha256(str(total).encode("utf-8")).hexdigest()
    print(digest)


if __name__ == "__main__":
    main()
