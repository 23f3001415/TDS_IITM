from __future__ import annotations

import csv
from pathlib import Path

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="GA2 Q13 FastAPI")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=["*"],
)

CSV_PATH = Path(__file__).with_name("q-fastapi.csv")


def load_students() -> list[dict[str, object]]:
    students: list[dict[str, object]] = []
    with CSV_PATH.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            students.append(
                {
                    "studentId": int(row["studentId"]),
                    "class": row["class"],
                }
            )
    return students


STUDENTS = load_students()


@app.get("/api")
def get_students(class_: list[str] | None = Query(default=None, alias="class")) -> dict[str, list[dict[str, object]]]:
    if not class_:
        return {"students": STUDENTS}

    wanted = set(class_)
    filtered = [student for student in STUDENTS if student["class"] in wanted]
    return {"students": filtered}