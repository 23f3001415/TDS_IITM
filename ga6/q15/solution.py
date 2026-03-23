import math


COVERAGE_DATA = {
    "executed_lines": [
        1, 24, 27, 29, 30, 31, 32, 33, 34, 35, 36, 37, 41, 44, 45, 47, 48, 49,
        52, 53, 54, 55, 56, 60, 64, 67, 70, 71, 72, 73, 74, 77, 78, 81, 84, 86,
        87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 98, 99, 102, 103, 104, 107,
    ],
    "missing_lines": [
        3, 4, 6, 9, 10, 12, 13, 14, 15, 16, 17, 18, 20, 21, 22, 23, 26, 28,
        40, 46, 57, 61, 68, 75, 76, 85, 97, 101,
    ],
    "branches": {
        "[52, 56]": True, "[71, 76]": True, "[56, 58]": True, "[34, 39]": True,
        "[61, 65]": True, "[34, 35]": True, "[18, 19]": True, "[104, 107]": False,
        "[10, 15]": True, "[14, 15]": False, "[14, 17]": True, "[71, 74]": True,
        "[99, 103]": True, "[27, 30]": True, "[76, 80]": True, "[91, 93]": True,
        "[33, 38]": True, "[41, 46]": True, "[40, 45]": False, "[17, 19]": True,
        "[26, 31]": True, "[34, 38]": True, "[91, 95]": True, "[37, 38]": True,
        "[30, 31]": True, "[88, 93]": True, "[75, 77]": False, "[84, 88]": False,
        "[61, 63]": False, "[55, 57]": False, "[47, 48]": False, "[46, 51]": False,
        "[10, 12]": False, "[36, 37]": False, "[60, 62]": False, "[16, 19]": False,
        "[6, 7]": False, "[92, 96]": False, "[28, 29]": False, "[12, 17]": False,
        "[60, 64]": False, "[67, 69]": False, "[81, 82]": False, "[75, 76]": False,
        "[12, 14]": False, "[57, 62]": False,
    },
    "total_statements": 80,
    "total_branches": 50,
}


def main() -> None:
    line_coverage_pct = len(COVERAGE_DATA["executed_lines"]) / COVERAGE_DATA["total_statements"] * 100
    branch_coverage_pct = (
        sum(1 for v in COVERAGE_DATA["branches"].values() if v) / COVERAGE_DATA["total_branches"] * 100
    )

    missing = sorted(COVERAGE_DATA["missing_lines"])
    groups = []
    current = [missing[0]]
    for line in missing[1:]:
        if line == current[-1] + 1:
            current.append(line)
        else:
            groups.append(current)
            current = [line]
    groups.append(current)

    missing_line_runs = sum(math.ceil(len(group) / 4) for group in groups)
    critical_missing = max(len(group) for group in groups)

    print(f"{line_coverage_pct:.2f},{branch_coverage_pct:.2f},{missing_line_runs},{critical_missing}")


if __name__ == "__main__":
    main()
