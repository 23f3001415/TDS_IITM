import re
from typing import List

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


app = FastAPI(title="Batch Sentiment API", version="1.2.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


class SentimentRequest(BaseModel):
    sentences: List[str] = Field(default_factory=list)


class SentimentItem(BaseModel):
    sentence: str
    sentiment: str


class SentimentResponse(BaseModel):
    results: List[SentimentItem]


analyzer = SentimentIntensityAnalyzer()

POSITIVE_PHRASES = {
    "not bad",
    "well done",
    "great job",
    "love it",
    "very good",
}

NEGATIVE_PHRASES = {
    "not good",
    "not great",
    "not happy",
    "could be better",
    "fed up",
    "very bad",
}

STRONG_POSITIVE = {
    "love",
    "amazing",
    "awesome",
    "great",
    "excellent",
    "fantastic",
    "wonderful",
    "happy",
    "delighted",
    "thrilled",
    "pleased",
    "good",
    "best",
    "enjoy",
}

STRONG_NEGATIVE = {
    "hate",
    "terrible",
    "awful",
    "bad",
    "worst",
    "horrible",
    "sad",
    "angry",
    "upset",
    "disappointed",
    "frustrated",
    "poor",
    "unhappy",
    "depressed",
}

NEGATIONS = {"not", "never", "no", "hardly", "barely", "without"}


def _has_local_negation(tokens: List[str], idx: int) -> bool:
    left = max(0, idx - 2)
    window = tokens[left:idx]
    return any(tok in NEGATIONS or tok.endswith("n't") for tok in window)


def classify_sentiment(sentence: str) -> str:
    text = (sentence or "").strip().lower()
    if not text:
        return "neutral"

    for phrase in NEGATIVE_PHRASES:
        if phrase in text:
            return "sad"
    for phrase in POSITIVE_PHRASES:
        if phrase in text:
            return "happy"

    tokens = re.findall(r"[a-z']+", text)
    for idx, tok in enumerate(tokens):
        negated = _has_local_negation(tokens, idx)
        if tok in STRONG_POSITIVE:
            return "sad" if negated else "happy"
        if tok in STRONG_NEGATIVE:
            return "happy" if negated else "sad"

    compound = analyzer.polarity_scores(text)["compound"]
    if compound >= 0.02:
        return "happy"
    if compound <= -0.02:
        return "sad"
    return "neutral"


@app.get("/")
def root() -> dict:
    return {"status": "ok", "endpoint": "/sentiment"}


@app.post("/sentiment", response_model=SentimentResponse)
def sentiment_batch(payload: SentimentRequest) -> SentimentResponse:
    results = [
        SentimentItem(sentence=sentence, sentiment=classify_sentiment(sentence))
        for sentence in payload.sentences
    ]
    return SentimentResponse(results=results)
