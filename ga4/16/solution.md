# Question 16: Cross-Lingual Entity Disambiguation

## Final Answer
Submit the CSV mapping from:

- [output.csv](C:\Users\sriva\OneDrive\Documents\TDS\ga4\16\output.csv)

It contains exactly 1000 mappings in `doc_id,entity_id` format.

## ELI15 Step-by-Step (for a complete novice)
1. Unzip the dataset and open:
   - `documents.jsonl`
   - `entity_reference.csv`
2. For each document, read:
   - `doc_id`, `mentioned_name`, `year`, `source_region`
3. Use region as the first filter:
   - Many regions map to exactly one entity directly.
4. For ambiguous regions (France, Russia, England), use year ranges.
5. For overlap years, disambiguate with ordinal clues in `mentioned_name`:
   - `I/II/III/IV`
   - `1/2/3/4`
   - cross-lingual forms like Arabic/CJK/Korean ordinal markers.
6. Apply typo-tolerant matching for Latin variants (`Alexandre`, `Alejandro`, etc.).
7. Write final strict CSV with:
   - `doc_id,entity_id`
8. Validate:
   - exactly 1000 rows
   - every `doc_id` appears once.

## Repro script
- [disambiguate.py](C:\Users\sriva\OneDrive\Documents\TDS\ga4\16\disambiguate.py)

Run:
```bash
python disambiguate.py
```
