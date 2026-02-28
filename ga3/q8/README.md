# Q8: Browser Runtime Diagnostics using DevTools Instrumentation

## ELI15 Step-by-Step (Beginner Friendly)

1. This task cannot be solved with `requests` or BeautifulSoup because runtime errors happen inside the browser.
2. Use Playwright (real browser automation).
3. Open your personalized URL:
   `https://sanand0.github.io/tdsdata/cdp_trap/index.html?student=23f3001415%40ds.study.iitm.ac.in`
4. Visit all 15 pages by following links.
5. Listen to:
   - `console` events (for logs/warnings/debug)
   - `pageerror` events (for uncaught JS exceptions)
6. Wait ~3.5 seconds on each page to catch delayed async errors.
7. Count only pages where `pageerror` happened.
8. Report:
   - total pages visited
   - total error pages
   - first error page in visit order

## Run Commands

```powershell
cd ga3/q8
npm init -y
npm i playwright
npx playwright install chromium
node diagnose.js
```

## Final Answer (for grader)

Use the 3 output lines printed by `node diagnose.js` exactly.

Current run output:

```text
TOTAL_PAGES_VISITED=15
TOTAL_ERRORS=4
FIRST_ERROR_PAGE=page_3.html
```
