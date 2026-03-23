# /// script
# requires-python = ">=3.11"
# dependencies = ["openai", "pandas"]
# ///

from __future__ import annotations

import json
import os
import re
import time
from collections import Counter
from pathlib import Path
from typing import Iterable

import pandas as pd
from openai import OpenAI

VALID_LABELS = ["Politics", "Sports", "Technology", "Business", "Entertainment"]
VALID_SET = set(VALID_LABELS)
MODEL = "gpt-4o-mini"
BATCH_SIZE = 10


def load_dotenv_if_present() -> None:
    env_path = Path(__file__).resolve().parent / ".env"
    if not env_path.exists():
        return
    for raw in env_path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and value and key not in os.environ:
            os.environ[key] = value


def normalize_label(text: str) -> str | None:
    clean = re.sub(r"[^A-Za-z]", "", (text or "").strip()).lower()
    mapping = {
        "politics": "Politics",
        "political": "Politics",
        "sports": "Sports",
        "sport": "Sports",
        "technology": "Technology",
        "tech": "Technology",
        "business": "Business",
        "entertainment": "Entertainment",
        "entertainments": "Entertainment",
    }
    return mapping.get(clean)


def create_client() -> OpenAI:
    api_key = (
        os.getenv("OPENAI_API_KEY")
        or os.getenv("AIPIPE_TOKEN")
        or os.getenv("AIPROXY_TOKEN")
    )
    if not api_key:
        raise RuntimeError(
            "Missing API key/token. Set OPENAI_API_KEY (or AIPIPE_TOKEN/AIPROXY_TOKEN)."
        )
    base_url = os.getenv("OPENAI_BASE_URL")
    if not base_url and (os.getenv("AIPIPE_TOKEN") or os.getenv("AIPROXY_TOKEN")):
        base_url = "https://aipipe.org/openai/v1"
    return OpenAI(api_key=api_key, base_url=base_url) if base_url else OpenAI(api_key=api_key)


def parse_labels(text: str, expected_count: int) -> list[str] | None:
    payload = None
    try:
        payload = json.loads(text)
    except json.JSONDecodeError:
        match = re.search(r"\{[\s\S]*\}|\[[\s\S]*\]", text)
        if match:
            try:
                payload = json.loads(match.group(0))
            except json.JSONDecodeError:
                payload = None

    labels_raw: Iterable[str] | None = None
    if isinstance(payload, dict) and isinstance(payload.get("labels"), list):
        labels_raw = payload["labels"]
    elif isinstance(payload, list):
        labels_raw = payload

    if labels_raw is None:
        return None

    labels = []
    for item in labels_raw:
        if not isinstance(item, str):
            return None
        normalized = normalize_label(item)
        if normalized is None:
            return None
        labels.append(normalized)

    if len(labels) != expected_count:
        return None
    if any(label not in VALID_SET for label in labels):
        return None
    return labels


def classify_single(client: OpenAI, headline: str) -> str:
    prompt = (
        "Classify this news headline into exactly one category from: "
        "Politics, Sports, Technology, Business, Entertainment.\n"
        "Reply with ONLY the category name.\n\n"
        f"Headline: {headline}"
    )
    for _ in range(3):
        response = client.chat.completions.create(
            model=MODEL,
            temperature=0,
            messages=[{"role": "user", "content": prompt}],
        )
        content = (response.choices[0].message.content or "").strip()
        normalized = normalize_label(content)
        if normalized in VALID_SET:
            return normalized
        time.sleep(1)

    # Last fallback: default to Business for unresolved finance/economy ambiguity
    return "Business"


def classify_batch(client: OpenAI, headlines: list[str]) -> list[str]:
    numbered = "\n".join(f"{i + 1}. {headline}" for i, headline in enumerate(headlines))
    prompt = (
        "Classify each headline into exactly one of these categories:\n"
        "- Politics\n- Sports\n- Technology\n- Business\n- Entertainment\n\n"
        "Return ONLY valid JSON in this exact format:\n"
        '{"labels":["Politics","Sports"]}\n'
        f"There must be exactly {len(headlines)} labels in the same order as input.\n\n"
        f"Headlines:\n{numbered}"
    )

    for _ in range(4):
        response = client.chat.completions.create(
            model=MODEL,
            temperature=0,
            messages=[{"role": "user", "content": prompt}],
        )
        content = response.choices[0].message.content or ""
        labels = parse_labels(content, expected_count=len(headlines))
        if labels is not None:
            return labels
        time.sleep(1)

    return [classify_single(client, headline) for headline in headlines]


def main() -> None:
    load_dotenv_if_present()
    client = create_client()

    base_dir = Path(__file__).resolve().parent
    input_path = base_dir / "q-topic-modeling-llm.csv"
    df = pd.read_csv(input_path)

    if "headline" not in df.columns:
        raise RuntimeError("Input CSV must contain a 'headline' column.")
    if df.shape[0] != 200:
        raise RuntimeError(f"Expected 200 headlines, found {df.shape[0]}.")

    headlines = df["headline"].astype(str).tolist()
    labels: list[str] = []

    for start in range(0, len(headlines), BATCH_SIZE):
        batch = headlines[start : start + BATCH_SIZE]
        labels.extend(classify_batch(client, batch))

    if len(labels) != len(headlines):
        raise RuntimeError("Label count mismatch after classification.")
    if any(label not in VALID_SET for label in labels):
        raise RuntimeError("Found invalid label outside required set.")

    df["topic"] = labels
    counts = Counter(labels)
    tech_count = int(counts["Technology"])

    df.to_csv(base_dir / "classified_headlines.csv", index=False)
    (base_dir / "answer.txt").write_text(f"{tech_count}\n", encoding="utf-8")

    print(counts)
    print(f"Technology count: {tech_count}")
    print(tech_count)


if __name__ == "__main__":
    main()

