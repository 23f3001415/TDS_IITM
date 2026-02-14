from __future__ import annotations

import json
import math
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

DATA_PATH = Path(__file__).resolve().parents[1] / "q-vercel-latency.json"

with DATA_PATH.open("r", encoding="utf-8") as f:
    TELEMETRY = json.load(f)


class MetricsRequest(BaseModel):
    regions: list[str] = Field(default_factory=list)
    threshold_ms: float


def percentile_95(values: list[float]) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    if len(ordered) == 1:
        return ordered[0]
    idx = 0.95 * (len(ordered) - 1)
    lo = math.floor(idx)
    hi = math.ceil(idx)
    if lo == hi:
        return ordered[lo]
    return ordered[lo] + (ordered[hi] - ordered[lo]) * (idx - lo)


def summarize_region(rows: list[dict], threshold_ms: float) -> dict[str, float | int]:
    latencies = [float(r["latency_ms"]) for r in rows]
    uptimes = [float(r["uptime_pct"]) for r in rows]
    breaches = sum(1 for r in rows if float(r["latency_ms"]) > threshold_ms)

    return {
        "avg_latency": sum(latencies) / len(latencies),
        "p95_latency": percentile_95(latencies),
        "avg_uptime": sum(uptimes) / len(uptimes),
        "breaches": breaches,
    }


app = FastAPI(title="GA2 Q14 Vercel Analytics")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["POST"],
    allow_headers=["*"],
)


@app.post("/")
@app.post("/api")
def analytics(payload: MetricsRequest) -> dict[str, dict[str, float | int]]:
    requested = set(payload.regions)
    filtered = [row for row in TELEMETRY if row.get("region") in requested]

    by_region: dict[str, list[dict]] = {}
    for row in filtered:
        region = row["region"]
        by_region.setdefault(region, []).append(row)

    result: dict[str, dict[str, float | int]] = {}
    for region, rows in by_region.items():
        result[region] = summarize_region(rows, payload.threshold_ms)
    return result