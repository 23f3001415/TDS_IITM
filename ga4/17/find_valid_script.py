import csv
import os
import tempfile
from pathlib import Path

import requests


SCRIPTS_DIR = Path(r"C:\Users\sriva\OneDrive\Documents\TDS\ga4\17\scripts")


class FakeResponse:
    def __init__(self):
        self.status_code = 200
        self.headers = {"Content-Type": "application/json"}

    def json(self):
        return {"ok": True, "id": 1}


def run_script(filepath: Path):
    code = filepath.read_text(encoding="utf-8")
    ns = {}
    try:
        exec(compile(code, str(filepath), "exec"), ns, ns)
    except Exception as e:
        return False, f"load:{type(e).__name__}:{e}"

    target_fn = None
    target_name = None
    for name in [
        "process_config",
        "fetch_user_data",
        "get_next_billing_date",
        "backup_log_file",
        "process_sales_data",
    ]:
        if name in ns and callable(ns[name]):
            target_name = name
            target_fn = ns[name]
            break

    if target_fn is None:
        return False, "no_known_function"

    try:
        if target_name == "process_config":
            target_fn('{"settings":{"theme":"dark"}}')
            target_fn('{"settings":{}}')
            target_fn("not valid json")

        elif target_name == "fetch_user_data":
            original_get = requests.get
            requests.get = lambda url: FakeResponse()
            try:
                target_fn("https://example.com/api", 123)
            finally:
                requests.get = original_get

        elif target_name == "get_next_billing_date":
            target_fn("2024-11-15")  # else branch
            target_fn("2024-12-15")  # if branch

        elif target_name == "backup_log_file":
            with tempfile.TemporaryDirectory() as d:
                log_dir = os.path.join(d, "logs")
                os.makedirs(log_dir, exist_ok=True)
                backup_dir = os.path.join(d, "backup")
                file_name = "a.log"
                with open(os.path.join(log_dir, file_name), "w", encoding="utf-8") as f:
                    f.write("line")
                target_fn(log_dir, file_name, backup_dir)

        elif target_name == "process_sales_data":
            with tempfile.TemporaryDirectory() as d:
                csv_path = os.path.join(d, "sales.csv")
                with open(csv_path, "w", newline="", encoding="utf-8") as f:
                    writer = csv.writer(f)
                    writer.writerow(["sales", "category", "revenue"])
                    writer.writerow([10, "A", 100])
                    writer.writerow([5, "B", 30])
                    writer.writerow([20, "A", 50])
                target_fn(csv_path, 7)

    except Exception as e:
        return False, f"run:{type(e).__name__}:{e}"

    return True, "ok"


def main():
    valid = []
    for fp in sorted(SCRIPTS_DIR.glob("script_*.py")):
        ok, _ = run_script(fp)
        if ok:
            valid.append(fp.name)

    print(valid)
    if len(valid) == 1:
        print(valid[0])


if __name__ == "__main__":
    main()
