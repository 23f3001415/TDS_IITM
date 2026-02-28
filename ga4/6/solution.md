# Question 6: JSON - Sensor Roll-up Analytics

## Final Answer (submit this)
`61.05`

## ELI15 Step-by-Step (for a complete novice)
1. Open the JSONL file `q-json-sensor-rollup.jsonl`.
2. Read it line-by-line (streaming), not all at once.
3. For each JSON record, keep only:
   - `site = Plant-02`
   - `device` starts with `condenser`
4. Keep only records between:
   - `2024-07-05T17:22:24.618Z`
   - `2024-07-10T17:22:24.618Z`
5. Remove records where `status` is `maintenance` or `offline`.
6. Read `metrics.temperature.value` and `metrics.temperature.unit`.
7. Convert Fahrenheit to Celsius using:
   - `C = (F - 32) * 5/9`
8. Compute the average of all Celsius temperatures that remain.
9. Round to 2 decimals.
10. Final average temperature is **`61.05 C`**.

## Validation snapshot
- Qualifying records after all filters: 1
- Average (C): 61.05
