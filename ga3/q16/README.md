# Q16: Scrape IMDb Movies

## ELI15 Step-by-Step

1. Open IMDb advanced title search with rating filter `2` to `7` (`/search/title/?user_rating=2,7`).
2. Download the HTML page in Python using a browser-like User-Agent.
3. Read IMDb's embedded `__NEXT_DATA__` JSON from the page.
4. Extract title entries from `titleListItems`.
5. Keep only movies with rating between `2` and `7`.
6. Build JSON objects with:
   - `id` (like `tt1234567`)
   - `title` (with rank prefix like `1. Movie Name`)
   - `year` (`YYYY` for films, `YYYY– ` for ongoing series)
   - `rating`
7. Return up to first 25 entries.

## Run

```powershell
pip install requests
python main.py
```

## Output

The script prints JSON array you can paste into the grader.
