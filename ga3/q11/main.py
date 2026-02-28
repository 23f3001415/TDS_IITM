from __future__ import annotations

import json
import os
import re
import sys
import time
from collections import OrderedDict
from typing import Any

from google import genai
from pydantic import BaseModel, Field


MODEL_NAME = "gemini-2.5-flash"
MAX_ATTENDEES = 20
PROCESS_TIMEOUT_SECONDS = 600


class Attendee(BaseModel):
    name: str = Field(description="Full name exactly as shown on screen.")
    date: str = Field(description="Date in dd/mm/yyyy format.")


class AttendeeResponse(BaseModel):
    attendees: list[Attendee]


def parse_json_array(text: str) -> list[dict[str, Any]]:
    raw = text.strip()
    if raw.startswith("["):
        return json.loads(raw)

    # Gemini can occasionally wrap JSON in extra words. Recover first array block.
    m = re.search(r"\[[\s\S]*\]", raw)
    if not m:
        raise ValueError("Model did not return a JSON array.")
    return json.loads(m.group(0))


def normalize_date(value: str) -> str | None:
    m = re.search(r"(\d{1,2})[/-](\d{1,2})[/-](\d{4})", value.strip())
    if not m:
        return None
    dd = int(m.group(1))
    mm = int(m.group(2))
    yyyy = int(m.group(3))
    if not (1 <= dd <= 31 and 1 <= mm <= 12 and 2000 <= yyyy <= 2100):
        return None
    return f"{dd:02d}/{mm:02d}/{yyyy:04d}"


def normalize_name(value: str) -> str | None:
    name = re.sub(r"\s+", " ", value.strip())
    name = re.sub(r"^[^A-Za-z]+", "", name)
    name = re.sub(r"[^A-Za-z .'-]+$", "", name)
    if len(name) < 3:
        return None
    if len(name.split()) < 2:
        return None
    return name


def clean_attendees(items: list[dict[str, Any]]) -> list[dict[str, str]]:
    unique: "OrderedDict[tuple[str, str], dict[str, str]]" = OrderedDict()
    for item in items:
        if not isinstance(item, dict):
            continue
        raw_name = str(item.get("name", ""))
        raw_date = str(item.get("date", ""))
        name = normalize_name(raw_name)
        date = normalize_date(raw_date)
        if not name or not date:
            continue
        key = (name.lower(), date)
        unique[key] = {"name": name, "date": date}
        if len(unique) >= MAX_ATTENDEES:
            break
    return list(unique.values())


def build_prompt(previous_json: str | None = None) -> str:
    base = """
You are extracting attendees from a ~44-second corporate check-in video.

Rules:
1) Watch the entire video timeline from start to end.
2) Check BOTH areas:
   - Center card: current attendee being checked in.
   - Right panel: recent check-ins that stay visible.
3) Output exactly 20 unique attendees.
4) Use exact spelling from the video.
5) Date format must be dd/mm/yyyy.
6) Return ONLY a JSON array:
   [{"name":"...","date":"dd/mm/yyyy"}, ...]
7) No markdown, no explanation, no extra keys.
"""
    if previous_json:
        return (
            base
            + "\nYou previously returned this partial list:\n"
            + previous_json
            + "\nNow correct it and return the full final 20 unique attendees."
        )
    return base


def generate_attendees(
    client: genai.Client,
    uploaded_file: Any,
    previous_json: str | None = None,
) -> list[dict[str, str]]:
    prompt = build_prompt(previous_json)
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=[uploaded_file, prompt],
        config={
            "temperature": 0.0,
            "response_mime_type": "application/json",
        },
    )
    data = parse_json_array(response.text or "[]")
    return clean_attendees(data)


def wait_until_active(client: genai.Client, uploaded_file: Any) -> Any:
    started = time.time()
    current = uploaded_file
    while getattr(current.state, "name", "") == "PROCESSING":
        if time.time() - started > PROCESS_TIMEOUT_SECONDS:
            raise TimeoutError("Timed out waiting for Gemini to process the video.")
        time.sleep(5)
        current = client.files.get(name=current.name)
    return current


def main() -> None:
    video_path = sys.argv[1] if len(sys.argv) > 1 else "attendee_checkin.webm"
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Video not found: {video_path}")

    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError("Set GEMINI_API_KEY first, then run the script again.")

    client = genai.Client(api_key=api_key)

    print("Uploading video to Gemini Files API...")
    uploaded = client.files.upload(file=video_path)
    uploaded = wait_until_active(client, uploaded)
    print("Video processed. Extracting attendees...")

    # Pass 1
    attendees = generate_attendees(client, uploaded)

    # Pass 2 (self-correction) if first pass is incomplete.
    if len(attendees) < MAX_ATTENDEES:
        previous = json.dumps(attendees, ensure_ascii=False)
        attendees = generate_attendees(client, uploaded, previous_json=previous)

    if len(attendees) < 15:
        raise RuntimeError(
            "Less than 15 valid attendees were extracted. "
            "Most common cause: incomplete recording (video did not reach 20/20). "
            "Regenerate the video, keep the tab active for ~44 seconds, and run again."
        )

    attendees = attendees[:MAX_ATTENDEES]
    print(json.dumps(attendees, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
