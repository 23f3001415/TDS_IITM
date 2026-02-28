# Q6: Data Sourcing with Google Dorks

## ELI15 Step-by-Step (Beginner Friendly)

1. We need one Google search query (called a "dork").
2. It must only search inside `worldbank.org`.
3. It must target downloadable dataset file types (`xlsx`, `csv`, `pdf`).
4. It must focus on **World Bank data for japan**.
5. Use multiple operators like:
   - `site:`
   - `filetype:`
   - `intitle:`
   - `inurl:`
   - `intext:`
6. Combine them into one query line.

## Final Answer (for grader)

`site:worldbank.org (filetype:xlsx OR filetype:csv OR filetype:pdf) intitle:"japan" inurl:data intext:"world bank data"`
