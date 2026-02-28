from __future__ import annotations

import json
import os
import re
from typing import Any

import requests

SAMPLE_TEXT = (
    "Trial NCT12345, Phase 3, 500 participants. "
    "Intervention: Drug A 100mg daily. "
    "Primary outcome: disease progression. "
    "Status: Recruiting"
)

SCHEMA: dict[str, Any] = {
    "type": "object",
    "properties": {
        "trialId": {"type": "string"},
        "phase": {"type": "string"},
        "participants": {"type": "number"},
        "intervention": {"type": "string"},
        "outcomes": {"type": "array", "items": {"type": "string"}},
        "status": {"type": "string"},
    },
    "required": ["trialId", "phase", "participants", "intervention"],
    "additionalProperties": False,
}


def regex_extract(text: str) -> dict[str, Any]:
    trial = re.search(r"\b(NCT\d+)\b", text, flags=re.IGNORECASE)
    phase = re.search(r"\b(Phase\s*\d+)\b", text, flags=re.IGNORECASE)
    participants = re.search(r"\b(\d+)\s+participants\b", text, flags=re.IGNORECASE)
    intervention = re.search(r"Intervention:\s*([^\.]+)", text, flags=re.IGNORECASE)
    outcome = re.search(r"Primary outcome:\s*([^\.]+)", text, flags=re.IGNORECASE)
    status = re.search(r"Status:\s*([^\.]+)", text, flags=re.IGNORECASE)

    out: dict[str, Any] = {}
    if trial:
        out["trialId"] = trial.group(1).upper()
    if phase:
        out["phase"] = re.sub(r"\s+", " ", phase.group(1)).strip().title()
    if participants:
        out["participants"] = int(participants.group(1))
    if intervention:
        out["intervention"] = intervention.group(1).strip()
    if outcome:
        out["outcomes"] = [outcome.group(1).strip()]
    if status:
        out["status"] = status.group(1).strip()
    return out


def llm_extract(text: str, token: str, feedback: str = "") -> dict[str, Any]:
    prompt = f"""
Extract clinical-trial fields from text and return only JSON.

Required fields:
- trialId (string)
- phase (string)
- participants (number)
- intervention (string)

Optional:
- outcomes (array of strings)
- status (string)

Rules:
- Keep values concise and exact.
- participants must be numeric.
- Do not invent data.
{feedback}

Text:
\"\"\"{text}\"\"\"
"""
    body = {
        "model": "gpt-4o-mini",
        "temperature": 0,
        "response_format": {"type": "json_object"},
        "messages": [
            {"role": "system", "content": "You are a precise data extraction engine."},
            {"role": "user", "content": prompt},
        ],
    }
    resp = requests.post(
        "https://aipipe.org/openai/v1/chat/completions",
        headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
        json=body,
        timeout=60,
    )
    resp.raise_for_status()
    content = resp.json()["choices"][0]["message"]["content"]
    return json.loads(content)


def validate_payload(extracted: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    props = SCHEMA["properties"]
    required = SCHEMA["required"]

    for field in required:
        if field not in extracted:
            errors.append(f"Missing required field: {field}")

    for key, value in extracted.items():
        if key not in props:
            errors.append(f"Unexpected field: {key}")
            continue
        expected = props[key]["type"]
        if expected == "string":
            if not isinstance(value, str) or not value.strip():
                errors.append(f"Invalid {key}: expected non-empty string")
        elif expected == "number":
            if not isinstance(value, (int, float)):
                errors.append(f"Invalid {key}: expected number")
        elif expected == "array":
            if not isinstance(value, list):
                errors.append(f"Invalid {key}: expected array")
            elif any(not isinstance(item, str) or not item.strip() for item in value):
                errors.append(f"Invalid {key}: array items must be non-empty strings")

    trial_id = extracted.get("trialId")
    if isinstance(trial_id, str) and not re.fullmatch(r"NCT\d{5,}", trial_id):
        errors.append("trialId format should look like NCT12345")

    return errors


def run_extraction(text: str) -> dict[str, Any]:
    token = os.getenv("AIPIPE_TOKEN", "").strip()
    retries = 0
    model_used = "regex-fallback"
    extracted: dict[str, Any] = {}
    errors: list[str] = []

    if token:
        feedback = ""
        for attempt in range(3):
            retries = attempt
            try:
                candidate = llm_extract(text, token, feedback)
                candidate_errors = validate_payload(candidate)
                if not candidate_errors:
                    extracted = candidate
                    errors = []
                    model_used = "gpt-4o-mini (via aipipe)"
                    break
                feedback = f"Previous validation errors: {candidate_errors}. Fix them."
                errors = candidate_errors
                extracted = candidate
            except Exception as exc:
                errors = [f"LLM extraction error: {exc}"]
                feedback = f"Previous failure: {exc}. Return valid JSON only."
        else:
            # Fall back if all retries fail.
            extracted = regex_extract(text)
            errors = validate_payload(extracted)
            model_used = "regex-fallback"
    else:
        extracted = regex_extract(text)
        errors = validate_payload(extracted)

    validated = len(errors) == 0
    confidence = 0.98 if (validated and model_used.startswith("gpt")) else 0.92 if validated else 0.5

    return {
        "schema": SCHEMA,
        "extracted": extracted,
        "validated": validated,
        "confidence": confidence,
        "errors": errors,
        "retryCount": retries,
        "model": model_used,
    }


if __name__ == "__main__":
    result = run_extraction(SAMPLE_TEXT)
    print(json.dumps(result, ensure_ascii=False, indent=2))
