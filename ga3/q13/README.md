# Q13: GitHub Action - Scrape Table Sums with Playwright

## ELI15 Step-by-Step

1. Create a repository and add a GitHub workflow under `.github/workflows/`.
2. Add a Node.js Playwright script that visits seed pages `70` to `79`.
3. For each page, read all table cells and sum all numeric values.
4. Add all page sums into one final total.
5. Print `FINAL_TOTAL_SUM=...` in workflow logs.
6. Ensure one workflow step name contains:
   `23f3001415@ds.study.iitm.ac.in`
7. Trigger the workflow and confirm it succeeds.
8. Submit repository URL + GitHub token in one line.

## Files

- `scripts/sum_tables.js`: Playwright scraper and sum calculator
- `.github/workflows/playwright-table-sum.yml`: GitHub Action workflow

## Verification

- Repository: `https://github.com/23f3001415/tds-ga3-q13-playwright-sum`
- Latest verified run: `https://github.com/23f3001415/tds-ga3-q13-playwright-sum/actions/runs/22312131111`
- Log includes:
  - step name with `23f3001415@ds.study.iitm.ac.in`
  - `FINAL_TOTAL_SUM=2530771`
