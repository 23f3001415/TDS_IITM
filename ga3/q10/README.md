# Q10: AI Expense Tracker - Multi-Page PDF Analysis

## ELI15 Step-by-Step (Beginner Friendly)

1. Make sure your PDF is downloaded (example: `expenses_23f3001415.pdf`).
2. Open terminal in `ga3/q10`.
3. Install dependency:
   ```powershell
   pip install pymupdf
   ```
4. Run:
   ```powershell
   python main.py "C:\Users\sriva\Downloads\expenses_23f3001415.pdf" "21Jan"
   ```
5. The script:
   - reads all 10 pages,
   - finds entries with 21st January in any `Jan/January` format,
   - converts Dollar/Dollars/USD to Rs using `1 USD = 80 Rs`,
   - sums all amounts and prints the total.
6. Paste that number in the grader.

## Final Answer (for your current downloaded PDF)

`216594`

