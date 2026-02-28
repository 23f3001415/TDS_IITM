from __future__ import annotations

import json
import re
import urllib.request
from dataclasses import dataclass
from typing import Any

import yt_dlp
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

app = FastAPI(title="GA3 Q7 YouTube Topic Timestamp API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class AskRequest(BaseModel):
    video_url: str = Field(min_length=1)
    topic: str = Field(min_length=1)


class AskResponse(BaseModel):
    timestamp: str
    video_url: str
    topic: str


@dataclass
class CaptionEntry:
    start_ms: int
    text: str


def normalize_text(value: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9 ]+", " ", value.lower())).strip()


def parse_timestamp_to_ms(value: str) -> int | None:
    m = re.match(r"^(?:(\d+):)?(\d{2}):(\d{2})[\.,](\d{3})$", value.strip())
    if not m:
        return None
    hours = int(m.group(1) or 0)
    minutes = int(m.group(2))
    seconds = int(m.group(3))
    millis = int(m.group(4))
    return ((hours * 60 + minutes) * 60 + seconds) * 1000 + millis


def ms_to_hhmmss(total_ms: int) -> str:
    total_seconds = max(0, total_ms // 1000)
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


def download_text(url: str) -> str:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0",
            "Accept": "text/vtt,application/json,text/plain,*/*",
        },
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8", errors="ignore")


def parse_vtt(content: str) -> list[CaptionEntry]:
    entries: list[CaptionEntry] = []
    lines = content.splitlines()
    i = 0

    while i < len(lines):
        line = lines[i].strip()
        if "-->" not in line:
            i += 1
            continue

        start_text = line.split("-->", 1)[0].strip().split(" ", 1)[0]
        start_ms = parse_timestamp_to_ms(start_text)

        i += 1
        parts: list[str] = []
        while i < len(lines) and lines[i].strip():
            if "-->" in lines[i]:
                break
            parts.append(lines[i].strip())
            i += 1

        if start_ms is not None and parts:
            text = re.sub(r"<[^>]+>", "", " ".join(parts)).strip()
            if text:
                entries.append(CaptionEntry(start_ms=start_ms, text=text))

        while i < len(lines) and lines[i].strip():
            i += 1
        i += 1

    return entries


def parse_json3(content: str) -> list[CaptionEntry]:
    entries: list[CaptionEntry] = []
    try:
        payload = json.loads(content)
    except json.JSONDecodeError:
        return entries

    for event in payload.get("events", []):
        start_ms = event.get("tStartMs")
        if not isinstance(start_ms, int):
            continue
        segs = event.get("segs") or []
        text = "".join(seg.get("utf8", "") for seg in segs if isinstance(seg, dict)).strip()
        text = re.sub(r"\s+", " ", text)
        if text:
            entries.append(CaptionEntry(start_ms=start_ms, text=text))

    return entries


def collect_caption_urls(info: dict[str, Any]) -> list[tuple[str, str]]:
    candidates: list[tuple[str, str, int]] = []

    def collect_from_tracks(tracks: dict[str, Any], base_priority: int) -> None:
        for lang, formats in (tracks or {}).items():
            if not isinstance(formats, list):
                continue
            lang_priority = 0 if lang.lower().startswith("en") else 50
            for item in formats:
                if not isinstance(item, dict):
                    continue
                url = item.get("url")
                ext = (item.get("ext") or "").lower()
                if not isinstance(url, str) or not url:
                    continue
                ext_priority = {"json3": 0, "vtt": 1, "srv3": 2, "ttml": 3}.get(ext, 10)
                candidates.append((url, ext, base_priority + lang_priority + ext_priority))

    collect_from_tracks(info.get("subtitles") or {}, base_priority=0)
    collect_from_tracks(info.get("automatic_captions") or {}, base_priority=20)

    candidates.sort(key=lambda x: x[2])
    return [(url, ext) for url, ext, _ in candidates]


def get_caption_entries(video_url: str) -> list[CaptionEntry]:
    ydl_opts: dict[str, Any] = {
        "quiet": True,
        "skip_download": True,
        "no_warnings": True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Failed to read video metadata: {exc}") from exc

    if not isinstance(info, dict):
        raise HTTPException(status_code=502, detail="Invalid metadata response from YouTube")

    for url, ext in collect_caption_urls(info):
        try:
            raw = download_text(url)
        except Exception:
            continue

        if ext == "json3":
            entries = parse_json3(raw)
        else:
            entries = parse_vtt(raw)

        if entries:
            return entries

    return []


def find_best_timestamp(entries: list[CaptionEntry], topic: str) -> int | None:
    if not entries:
        return None

    topic_norm = normalize_text(topic)
    if not topic_norm:
        return entries[0].start_ms

    topic_tokens = set(topic_norm.split())
    best_score = -1.0
    best_ms = None

    for entry in entries:
        text_norm = normalize_text(entry.text)
        if not text_norm:
            continue

        score = 0.0
        if topic_norm in text_norm:
            score += 100.0

        text_tokens = set(text_norm.split())
        if topic_tokens:
            overlap = len(topic_tokens & text_tokens) / len(topic_tokens)
            score += overlap * 10.0

        if score > best_score:
            best_score = score
            best_ms = entry.start_ms

    if best_ms is None:
        return entries[0].start_ms

    # If no meaningful overlap was found, return the first caption timestamp.
    if best_score < 1.0:
        return entries[0].start_ms

    return best_ms


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/ask", response_model=AskResponse)
def ask(payload: AskRequest) -> AskResponse:
    video_url = payload.video_url.strip()
    topic = payload.topic.strip()

    if not video_url or not topic:
        raise HTTPException(status_code=400, detail="video_url and topic are required")

    entries = get_caption_entries(video_url)
    if not entries:
        # Keep API contract stable even when subtitles are unavailable.
        return AskResponse(timestamp="00:00:00", video_url=video_url, topic=topic)

    timestamp_ms = find_best_timestamp(entries, topic)
    if timestamp_ms is None:
        timestamp_ms = 0

    return AskResponse(timestamp=ms_to_hhmmss(timestamp_ms), video_url=video_url, topic=topic)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8002, reload=False)
