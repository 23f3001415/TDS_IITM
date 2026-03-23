# /// script
# requires-python = ">=3.11"
# ///

from __future__ import annotations

import re
from pathlib import Path


def main() -> None:
    base_dir = Path(__file__).resolve().parent
    text = (base_dir / "company_policies.md").read_text(encoding="utf-8")

    match = re.search(
        r"hybrid work framework, employees may work remotely for up to \*\*(\d+) days per week\*\*",
        text,
        flags=re.IGNORECASE,
    )
    if not match:
        raise RuntimeError("Could not find hybrid work policy integer in handbook.")

    answer = match.group(1)
    (base_dir / "answer.txt").write_text(f"{answer}\n", encoding="utf-8")
    print(answer)


if __name__ == "__main__":
    main()

