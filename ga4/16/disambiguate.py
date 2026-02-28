import csv
import json
import re
from pathlib import Path


BASE_DIR = Path(r"C:\Users\sriva\OneDrive\Documents\TDS\ga4\16")
DOC_PATH = BASE_DIR / "documents.jsonl"
OUT_PATH = BASE_DIR / "output.csv"


def normalize_ascii(s):
    s = s.lower()
    s = re.sub(r"[^a-z0-9\s]+", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def ordinal_flags(name):
    nl = (name or "").lower()
    asc = normalize_ascii(name or "")
    esc = (name or "").encode("unicode_escape").decode("ascii").lower()

    first = second = third = fourth = False

    # Roman + common typo forms.
    if re.search(r"\bier\b|\beir\b", asc):
        first = True
    if re.search(r"\bii\b", asc):
        second = True
    if re.search(r"\biii\b", asc):
        third = True
    if re.search(r"\biv\b|\bi\s*v\b|\bi\s+v\b", asc):
        fourth = True
    if re.search(r"\bi\b", asc) and not re.search(r"\bii\b|\biii\b|\biv\b", asc):
        first = True

    # Arabic numerals.
    if re.search(r"(^|\D)1($|\D)", nl):
        first = True
    if re.search(r"(^|\D)2($|\D)", nl):
        second = True
    if re.search(r"(^|\D)3($|\D)", nl):
        third = True
    if re.search(r"(^|\D)4($|\D)", nl):
        fourth = True

    # CJK/Korean/Arabic ordinal words via escaped representation.
    if "\\u4e00\\u4e16" in esc or "1\\u4e16" in esc or "1\\uc138" in esc or "\\u0627\\u0644\\u0623\\u0648\\u0644" in esc:
        first = True
    if "\\u4e8c\\u4e16" in esc or "2\\u4e16" in esc or "2\\uc138" in esc or "\\u0627\\u0644\\u062b\\u0627\\u0646\\u064a" in esc:
        second = True
    if "\\u4e09\\u4e16" in esc or "3\\u4e16" in esc or "3\\uc138" in esc or "\\u0627\\u0644\\u062b\\u0627\\u0644\\u062b" in esc:
        third = True
    if "\\u56db\\u4e16" in esc or "4\\u4e16" in esc or "4\\uc138" in esc or "\\u0627\\u0644\\u0631\\u0627\\u0628\\u0639" in esc:
        fourth = True

    return first, second, third, fourth, asc, esc


def resolve_entity(doc):
    region = doc["source_region"]
    year = int(doc["year"])
    name = doc.get("mentioned_name", "")

    first, second, third, fourth, asc, esc = ordinal_flags(name)

    # Single-entity regions.
    if region == "Portugal":
        return "E001"
    if region == "Macedonia":
        return "E006"
    if region == "Prussia":
        return "E008"
    if region == "Holy Roman Empire":
        return "E012"
    if region == "Greece":
        return "E013"
    if region == "Spain":
        return "E015"

    # England: non-overlapping eras.
    if region == "England":
        if year <= 1200:
            return "E014"  # William I of England
        if year <= 1547:
            return "E009"  # Henry VIII of England
        return "E005"      # Charles I of England

    # France: Louis XVI / Louis XIV by year, else Henry IV vs Catherine de' Medici.
    if region == "France":
        if year >= 1754:
            return "E004"  # Louis XVI of France
        if 1638 <= year <= 1715:
            return "E007"  # Louis XIV of France

        henry_ascii = any(x in asc for x in [
            "henry", "henri", "enrique", "henrique", "henryk", "jindrich", "hendrik"
        ])
        henry_nonlatin = any(x in esc for x in [
            "\\u0647\\u0646\\u0631",              # Arabic Henry root
            "\\u0413\\u0435\\u043d\\u0440\\u0438\\u0445",  # Генрих
            "\\uc559\\ub9ac",                      # 앙리
            "\\u30a2\\u30f3\\u30ea",              # アンリ
            "\\u4ea8\\u5229",                      # 亨利
        ])
        if fourth or henry_ascii or henry_nonlatin:
            return "E016"  # Henry IV of France
        return "E011"      # Catherine de' Medici

    # Russia.
    if region == "Russia":
        if year <= 1584:
            return "E003"  # Ivan IV of Russia
        if year >= 1826:
            return "E010"  # Alexander II of Russia
        if 1797 <= year <= 1817:
            return "E017"  # Alexander I of Russia
        if 1763 <= year <= 1776:
            return "E018"  # Catherine the Great

        # 1728-1762: Peter III vs Catherine the Great.
        if 1728 <= year <= 1762:
            peter_ascii = any(x in asc for x in ["peter", "petr", "piotr", "pietro", "petro", "pedro"])
            if third or peter_ascii:
                return "E002"
            return "E018"

        # 1777-1796: Alexander I vs Catherine the Great.
        if 1777 <= year <= 1796:
            alex_ascii = any(x in asc for x in ["alexand", "aleksand", "alejandro", "alessandro", "alexandre"])
            if first or alex_ascii:
                return "E017"
            return "E018"

        # 1818-1825: Alexander I vs Alexander II.
        if 1818 <= year <= 1825:
            if second:
                return "E010"
            if first:
                return "E017"
            return "E017" if year <= 1821 else "E010"

    # Safety fallback.
    return "E001"


def main():
    rows = []

    with DOC_PATH.open("r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            doc = json.loads(line)
            rows.append((doc["doc_id"], resolve_entity(doc)))

    rows.sort(key=lambda x: x[0])

    with OUT_PATH.open("w", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["doc_id", "entity_id"])
        writer.writerows(rows)

    assert len(rows) == 1000
    assert len({doc_id for doc_id, _ in rows}) == 1000
    print(f"Wrote {OUT_PATH} with {len(rows)} rows.")


if __name__ == "__main__":
    main()
