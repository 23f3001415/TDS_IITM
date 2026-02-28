# Question 2: Excel - Z-Score Outlier Surveillance

## Final Answer (submit this)
`2`

## ELI15 Step-by-Step (for a complete novice)
1. Open Excel.
2. Go to `Data` -> `From Text/CSV` and import `q-excel-zscore-outlier.csv`.
3. Load it into a worksheet as a table.
4. Confirm the score column is numeric: `Customer_Satisfaction_Score`.
5. In an empty cell, compute mean (average):
   - `=AVERAGE(B2:B96)`
6. In another cell, compute sample standard deviation:
   - `=STDEV.S(B2:B96)`
7. Add a new column named `Z_Score`.
8. In the first data row of `Z_Score`, enter:
   - `=STANDARDIZE(B2,$E$2,$F$2)`
   Here, `E2` = mean and `F2` = `STDEV.S`.
9. Fill the formula down for all clinics.
10. Add another helper column `Outlier_Flag` with:
   - `=IF(ABS(C2)>=2.5,1,0)`
11. Fill down.
12. Count flagged clinics:
   - `=SUM(D2:D96)`
   (or directly: `=COUNTIFS(C2:C96,">=2.5")+COUNTIFS(C2:C96,"<=-2.5")`)
13. You get **2** clinics with `|z-score| >= 2.5`.

## Validation snapshot
- Total clinics: 95
- Mean score: 77.9553684211
- STDEV.S: 6.4171029472
- Outliers (`|z| >= 2.5`): 2
