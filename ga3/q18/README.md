# Q18: Clean Up Excel Sales Data

## ELI15 Step-by-Step

1. Open the Excel file in Python using `pandas`.
2. Trim spaces in text columns.
3. Standardize country values:
   - `UK`, `U.K`, `United Kingdom` -> `UK`
   - Similar cleanup for `US`, `FR`, `BR`, `IN`, `AE`.
4. Standardize dates:
   - `MM-DD-YYYY` and `YYYY/MM/DD` -> real datetime values.
5. Extract product name by taking text before `/` from `Product/Code`.
6. Clean `Sales` and `Cost` by removing `USD` and extra spaces.
7. If `Cost` is missing, set it to `50%` of `Sales`.
8. Filter rows where:
   - `Date <= 2022-08-25 14:57:47`
   - `Product == Alpha`
   - `Country == UK`
9. Compute:
   - `Total Sales = sum(Sales)`
   - `Total Cost = sum(Cost)`
   - `Margin = (Total Sales - Total Cost) / Total Sales`

## Run

```powershell
pip install pandas openpyxl
python main.py "C:\Users\sriva\Downloads\q-clean-up-excel-sales-data.xlsx"
```

## Final Answer

- Decimal: `0.282277859597`
- Percent: `28.227786%`
