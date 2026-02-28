# Question 10: Google Sheets - AI Formula Zip Extraction

## Final Answer (paste this concatenated string)
`62704,48202,19102,43085,N/A,60601,19101,28203,19101,90210,33101,48202,28203,62704,48201,N/A,43086,30302,19101,19102,48202,N/A,N/A,30301,N/A,N/A,94105,94105,77001,N/A,N/A,43086,43086,N/A,N/A,10001,28203,30302,33102,33102,N/A,30301,N/A,N/A,43085,33101,48202,19102,19102,10002,94105,N/A,10001,19101,43086,N/A,N/A,30301,N/A,28202,28203,19102,94105,28203,N/A,N/A,19101,30302,N/A,N/A,19102,48202,43086,33102,19102,48201,30302,19102,19102,28202,75001,33101,N/A,N/A,N/A,N/A,43085,77001,19101,N/A,30301,48202,43085,N/A,10001,77001,19102,77001,30302,75001`

## ELI15 Step-by-Step (for a complete novice)
1. Import `addresses_23f3001415@ds.study.iitm.ac.in.csv` into Google Sheets.
2. Keep addresses in column `A` (from `A2` to `A101`).
3. In `B2`, use:
   - `=AI("Extract the zip code (or postal code) from this address. If none exists, return N/A: " & A2)`
4. Fill the formula down to `B101`.
5. In a new cell, run:
   - `=TEXTJOIN(",", TRUE, B2:B101)`
6. Copy that final text and submit it.

## Validation snapshot
- Total rows processed: 100
- Rows with no zip/postal code (`N/A`): 27
