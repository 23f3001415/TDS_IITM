from __future__ import annotations

import csv
import io
from decimal import Decimal, InvalidOperation
from pathlib import Path

from fastapi import FastAPI, File, Header, HTTPException, Response, UploadFile
from fastapi.middleware.cors import CORSMiddleware

EMAIL = "23f3001415@ds.study.iitm.ac.in"
TOKEN = "wrbu8ux9frfk15td"
TOKEN_HEADER = "X-Upload-Token-4193"
MAX_FILE_SIZE_BYTES = 63 * 1024
ALLOWED_EXTENSIONS = {".csv", ".json", ".txt"}

app = FastAPI(title="GA2 Q18 FastAPI File Validation Service")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["POST", "OPTIONS"],
    allow_headers=["*"],
)


@app.middleware("http")
async def force_cors_headers(request, call_next):
    response = await call_next(request)
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "POST, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = f"Content-Type, {TOKEN_HEADER}"
    return response


@app.options("/")
@app.options("/api")
def preflight() -> Response:
    return Response(status_code=204)


def _analyze_csv(data: bytes, filename: str) -> dict[str, object]:
    try:
        text = data.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        raise HTTPException(status_code=400, detail="CSV must be UTF-8 text") from exc

    reader = csv.DictReader(io.StringIO(text))
    if not reader.fieldnames:
        raise HTTPException(status_code=400, detail="Invalid CSV: missing header row")

    rows = 0
    total_value = Decimal("0")
    category_counts: dict[str, int] = {}
    for row in reader:
        rows += 1
        value_raw = str(row.get("value", "")).strip()
        category = str(row.get("category", "")).strip()
        try:
            total_value += Decimal(value_raw)
        except InvalidOperation as exc:
            raise HTTPException(status_code=400, detail="Invalid CSV: non-numeric value column") from exc

        if category not in category_counts:
            category_counts[category] = 0
        category_counts[category] += 1

    return {
        "email": EMAIL,
        "filename": filename,
        "rows": rows,
        "columns": reader.fieldnames,
        "totalValue": round(float(total_value), 2),
        "categoryCounts": category_counts,
    }


@app.post("/")
@app.post("/api")
async def validate_and_process(
    file: UploadFile = File(...),
    x_upload_token_4193: str | None = Header(default=None, alias=TOKEN_HEADER),
) -> dict[str, object]:
    if x_upload_token_4193 != TOKEN:
        raise HTTPException(status_code=401, detail="Unauthorized")

    filename = file.filename or "uploaded-file"
    extension = Path(filename).suffix.lower()
    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Invalid file type")

    data = await file.read()
    if len(data) > MAX_FILE_SIZE_BYTES:
        raise HTTPException(status_code=413, detail="File too large")

    if extension == ".csv":
        return _analyze_csv(data=data, filename=filename)

    return {
        "email": EMAIL,
        "filename": filename,
        "message": "File accepted",
    }
