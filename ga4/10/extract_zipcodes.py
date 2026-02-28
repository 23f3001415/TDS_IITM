import re
import pandas as pd


FILE_PATH = r"C:\Users\sriva\Downloads\addresses_23f3001415@ds.study.iitm.ac.in.csv"
ZIP_PATTERN = re.compile(r"\b(\d{5})\b")


def main():
    df = pd.read_csv(FILE_PATH)
    results = []

    for address in df["address"]:
        text = str(address)
        match = ZIP_PATTERN.search(text)
        results.append(match.group(1) if match else "N/A")

    print(",".join(results))


if __name__ == "__main__":
    main()
