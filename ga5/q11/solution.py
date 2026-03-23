# /// script
# requires-python = ">=3.11"
# ///

from __future__ import annotations

import sqlite3
from pathlib import Path


def main() -> None:
    base_dir = Path(__file__).resolve().parent
    sql_path = base_dir / "q-datasette-sales-summary.sql"
    db_path = base_dir / "q-datasette-sales-summary.db"

    if db_path.exists():
        db_path.unlink()

    script = sql_path.read_text(encoding="utf-8")

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.executescript(script)

    row = cur.execute(
        """
        SELECT city, SUM(quantity * unit_price) AS total_revenue
        FROM orders
        WHERE LOWER(status) = 'delivered'
        GROUP BY city
        ORDER BY total_revenue DESC
        LIMIT 1
        """
    ).fetchone()

    if row is None:
        raise RuntimeError("No delivered orders found.")

    city = str(row[0])
    (base_dir / "answer.txt").write_text(f"{city}\n", encoding="utf-8")
    print(city)

    conn.close()


if __name__ == "__main__":
    main()

