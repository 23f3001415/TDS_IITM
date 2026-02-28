from __future__ import annotations

import json
import re
from typing import Any

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="GA3 Q12 Function Calling Router")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


def build_response(name: str, arguments: dict[str, Any]) -> dict[str, str]:
    return {"name": name, "arguments": json.dumps(arguments)}


def extract_employee_id(query: str) -> int | None:
    m = re.search(r"\b(?:employee|emp)\s*#?\s*(\d+)\b", query, flags=re.IGNORECASE)
    if m:
        return int(m.group(1))
    return None


def parse_function_call(q: str) -> dict[str, str]:
    query = q.strip()
    lower = query.lower()

    if "ticket" in lower:
        m = re.search(r"\bticket(?:\s*id)?\s*#?\s*(\d+)\b", query, flags=re.IGNORECASE)
        if not m:
            m = re.search(r"\b(\d+)\b", query)
        if m:
            ticket_id = int(m.group(1))
            return build_response("get_ticket_status", {"ticket_id": ticket_id})

    if "meeting" in lower or "schedule" in lower:
        date_m = re.search(r"\b(\d{4}-\d{2}-\d{2})\b", query)
        time_m = re.search(r"\b(\d{1,2}:\d{2})\b", query)
        room_m = re.search(r"\bin\s+(.+?)[\.\?]?$", query, flags=re.IGNORECASE)
        if not room_m and time_m:
            tail = query[time_m.end() :].strip()
            tail = re.sub(r"^(?:in|at)\s+", "", tail, flags=re.IGNORECASE)
            tail = tail.rstrip(".!? ").strip()
            if tail:
                room_m = re.match(r"(.+)", tail)
        if date_m and time_m and room_m:
            date = date_m.group(1)
            time = time_m.group(1)
            meeting_room = room_m.group(1).strip()
            return build_response(
                "schedule_meeting",
                {
                    "date": date,
                    "time": time,
                    "meeting_room": meeting_room,
                },
            )

    if "expense" in lower:
        employee_id = extract_employee_id(query)
        if employee_id is None:
            m = re.search(r"\b(\d+)\b", query)
            if m:
                employee_id = int(m.group(1))
        if employee_id is not None:
            return build_response("get_expense_balance", {"employee_id": employee_id})

    if "bonus" in lower:
        employee_id = extract_employee_id(query)
        year_m = re.search(r"\b(20\d{2})\b", query)

        # Fallbacks for shortened forms like "Calculate bonus for emp 23719 in 2025".
        nums = [int(n) for n in re.findall(r"\b\d+\b", query)]
        if employee_id is None and nums:
            for n in nums:
                if n < 2000:
                    employee_id = n
                    break
        year = int(year_m.group(1)) if year_m else None
        if year is None and nums:
            for n in nums:
                if 2000 <= n <= 2100:
                    year = n
                    break

        if employee_id is not None and year is not None:
            return build_response(
                "calculate_performance_bonus",
                {"employee_id": employee_id, "current_year": year},
            )

    if "issue" in lower:
        issue_m = re.search(r"\bissue(?:\s*code)?\s*#?\s*(\d+)\b", query, flags=re.IGNORECASE)
        if not issue_m:
            issue_m = re.search(r"\b(\d+)\b", query)
        dept_m = re.search(
            r"\bfor\s+(?:the\s+)?(.+?)\s+department\b",
            query,
            flags=re.IGNORECASE,
        )
        if not dept_m:
            dept_m = re.search(r"\bdepartment\s+(.+?)[\.\?]?$", query, flags=re.IGNORECASE)
        if issue_m and dept_m:
            issue_code = int(issue_m.group(1))
            department = dept_m.group(1).strip().rstrip(".!? ")
            return build_response(
                "report_office_issue",
                {"issue_code": issue_code, "department": department},
            )

    # Keep a non-error JSON response for unexpected probes.
    return build_response("unknown", {})


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/execute")
def execute(q: str = Query(default="", min_length=0)) -> dict[str, str]:
    if not q.strip():
        return build_response("unknown", {})
    return parse_function_call(q)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8003, reload=False)
