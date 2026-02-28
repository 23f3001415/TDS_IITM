# Question 17: LLM Hallucination Trap Matrix

## Final Answer (submit this filename)
`script_458.py`

## ELI15 Step-by-Step (for a complete novice)
1. Unzip the archive so you can access all 1000 scripts.
2. For each script, load the code and execute it in a safe test harness.
3. Identify the function in the script (`process_config`, `fetch_user_data`, `get_next_billing_date`, `backup_log_file`, or `process_sales_data`).
4. Call that function with controlled test inputs that force both normal and edge paths.
5. Use mocks where needed:
   - Mock `requests.get` so no real network call happens.
   - Use temporary files for file/CSV functions.
6. If a script calls a fake method (`json.parse`, `df.drop_nulls`, `requests.fetch`, etc.), it throws an error and is rejected.
7. Keep only scripts that run without any hallucination error.
8. Exactly one script remains valid: **`script_458.py`**.

## Repro script
- [find_valid_script.py](C:\Users\sriva\OneDrive\Documents\TDS\ga4\17\find_valid_script.py)
