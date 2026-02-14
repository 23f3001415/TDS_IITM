# Q5 Host a JSON Data API on GitHub Pages - ELI15 Step-by-Step

1. Create `ga2/q5/products.json` in your GitHub repo.
2. Add `metadata` with:
   - `email`: `23f3001415@ds.study.iitm.ac.in`
   - `version`: `bf25f036`
3. Add exactly 21 items in `products` with fields:
   - `id`, `name`, `category`, `price`, `stock`, `rating`
4. Add `aggregations` for categories.
5. Ensure `books` has:
   - `count: 3`
   - `inventoryValue: 103372.08`
6. Commit and push:
```powershell
git add ga2/q5/products.json
git commit -m "Add Q5 static JSON API for product catalog"
git push
```
7. Open GitHub Pages URL:
`https://23f3001415.github.io/TDS_IITM/ga2/q5/products.json`
8. If stale, use cache busting:
`...?v=1`

## Final URL format to submit
`https://23f3001415.github.io/TDS_IITM/ga2/q5/products.json`
