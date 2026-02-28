# Question 15: The Recursive Corrupted JSON Fixer

## Final Answer (submit only this SHA-256 hash)
`f9ca05cb536d326f278cceb4f5a2bd4d8d545b7ffca16fdfd6400a0086c47496`

## ELI15 Step-by-Step (for a complete novice)
1. Open the ZIP file (`corrupted_logs.zip`) without loading everything into memory.
2. Read `corrupted_logs.json` line-by-line as a stream.
3. For each line:
   - Try `json.loads(line)`.
   - If parsing fails, ignore that line (it is corrupted).
4. From valid JSON records only, read deeply nested:
   - `context.system.process.metrics.metric_2900`
5. Keep only integer values and add them to a running total.
6. Convert the final integer sum to text.
7. Compute SHA-256 hash of that text (no newline).
8. Submit the 64-character hex hash.

## Validation snapshot
- Valid JSON lines processed: 72107
- Corrupted lines skipped: 64983
- Integer sum of `metric_2900`: 35919751
- SHA-256: `f9ca05cb536d326f278cceb4f5a2bd4d8d545b7ffca16fdfd6400a0086c47496`
