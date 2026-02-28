# Q15: Count Crawled HTML Files

## ELI15 Step-by-Step

1. Start from `https://sanand0.github.io/tdsdata/crawl_html/`.
2. Crawl links recursively only within that path.
3. Collect all `.html` file URLs.
4. For each file name, check its first letter.
5. Count files starting with letters `M` to `Z` (case-insensitive).

## Run

```powershell
python count_m_to_z.py
```

## Final Answer

`66`

