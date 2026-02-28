# Q1: FIFA World Cup Data Cross-Table Analysis

## ELI15 Step-by-Step (Beginner Friendly)

1. Open this page in your browser:  
   `https://en.wikipedia.org/wiki/FIFA_World_Cup`
2. Open a new Google Sheet.
3. In `Sheet1`, cell `A1`, paste:
   ```excel
   =IMPORTHTML("https://en.wikipedia.org/wiki/FIFA_World_Cup","table",5)
   ```
4. Wait for the table to load. This should be the **Teams reaching the top four** table.
5. Find the row for **Brazil**.
6. Read the value in the **Top 4 total** column.  
   Result: `11`
7. In `Sheet2`, cell `A1`, paste:
   ```excel
   =IMPORTHTML("https://en.wikipedia.org/wiki/FIFA_World_Cup","table",7)
   ```
8. Wait for the table to load. This should be the **Top goalscorers** table.
9. Find the row for **Miroslav Klose**.
10. Read the value in the **Goals** column.  
    Result: `16`
11. Combine both results exactly as comma-separated numbers:
    `11,16`

## Final Answer (for grader)

`11,16`

## Notes

- If table numbers (`5`, `7`) return the wrong table, check nearby indices (`4`, `6`, `8`) because Wikipedia table order can shift slightly.
- Keep no spaces in the final submission unless the grader explicitly allows spaces.

