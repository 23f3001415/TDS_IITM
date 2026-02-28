import json
import zipfile
from collections import Counter


ZIP_PATH = r"C:\Users\sriva\Downloads\api_data_23f3001415@ds.study.iitm.ac.in.zip"


def main():
    counts = Counter()

    with zipfile.ZipFile(ZIP_PATH) as zf:
        for name in zf.namelist():
            if not name.lower().endswith(".json"):
                continue
            data = json.loads(zf.read(name))
            records = data if isinstance(data, list) else [data]
            for rec in records:
                level = ((rec or {}).get("metrics") or {}).get("level")
                if level is None:
                    continue
                lvl = int(level)
                if 1 <= lvl <= 10:
                    counts[lvl] += 1

    print("|".join(f"level{i}:{counts[i]}" for i in range(1, 11)))


if __name__ == "__main__":
    main()
