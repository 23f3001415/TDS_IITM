import argparse
import json
import re
from decimal import Decimal, ROUND_HALF_UP

import requests


IMDB_SEARCH_URL = "https://www.imdb.com/search/title/?user_rating=2,7"


def format_rating(value: object) -> str:
    # Match IMDb-like display rounding to one decimal place.
    rounded = Decimal(str(value)).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP)
    return f"{rounded:.1f}"


def extract_titles(html: str, min_rating: float, max_rating: float, limit: int) -> list[dict[str, str]]:
    match = re.search(
        r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>',
        html,
        flags=re.DOTALL,
    )
    if not match:
        raise RuntimeError("Could not find IMDb embedded JSON data.")

    payload = json.loads(match.group(1))
    items = (
        payload.get("props", {})
        .get("pageProps", {})
        .get("searchResults", {})
        .get("titleResults", {})
        .get("titleListItems", [])
    )
    if not items:
        raise RuntimeError("No title items found in IMDb response.")

    output: list[dict[str, str]] = []
    rank = 1
    for item in items:
        rating = item.get("ratingSummary", {}).get("aggregateRating")
        if rating is None:
            continue
        rating_value = float(rating)
        if rating_value < min_rating or rating_value > max_rating:
            continue

        output.append(
            {
                "id": str(item.get("titleId", "")),
                "title": f"{rank}. {str(item.get('titleText', ''))}",
                "year": format_year(item),
                "rating": format_rating(rating),
            }
        )
        rank += 1
        if len(output) >= limit:
            break

    return output


def format_year(item: dict) -> str:
    start_year = item.get("releaseYear")
    if start_year is None:
        return ""

    title_type = item.get("titleType", {}) or {}
    can_have_episodes = bool(title_type.get("canHaveEpisodes"))
    end_year = item.get("endYear")

    if can_have_episodes:
        if end_year is None:
            return f"{start_year}\u2013 "
        return f"{start_year}\u2013{end_year}"

    return str(start_year)


def main() -> None:
    parser = argparse.ArgumentParser(description="Scrape IMDb titles and print JSON output.")
    parser.add_argument("--limit", type=int, default=25, help="Maximum number of titles to output.")
    parser.add_argument("--min-rating", type=float, default=2.0, help="Minimum IMDb rating.")
    parser.add_argument("--max-rating", type=float, default=7.0, help="Maximum IMDb rating.")
    parser.add_argument("--url", default=IMDB_SEARCH_URL, help="IMDb search URL.")
    args = parser.parse_args()

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/122.0.0.0 Safari/537.36"
        ),
        "Accept-Language": "en-US,en;q=0.9",
    }
    response = requests.get(args.url, headers=headers, timeout=45)
    response.raise_for_status()

    result = extract_titles(
        html=response.text,
        min_rating=args.min_rating,
        max_rating=args.max_rating,
        limit=args.limit,
    )
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
