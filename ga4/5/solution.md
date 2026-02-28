# Question 5: OpenRefine - Supplier Spend Consolidation

## Final Answer (submit this)
`49143.64`

## ELI15 Step-by-Step (for a complete novice)
1. Open OpenRefine and import `q-openrefine-supplier-spend.csv`.
2. In each text column (`invoice_id`, `supplier_name`, `category`, `status`, `comment`), run:
   - `Edit cells` -> `Common transforms` -> `Trim leading and trailing whitespace`.
3. Clean `supplier_name`:
   - Open the `supplier_name` column menu.
   - Run `Edit cells` -> `Cluster and edit...`.
   - Use key-collision methods and nearest-neighbour methods.
   - Merge all Zenith variants into one canonical value: `Zenith Components` (examples: `Zenith Comp.`, `Zenith Component`, `Zenith-Components`, `ZenithComponents`).
4. Remove duplicate invoices:
   - Create a text facet on `invoice_id`.
   - For duplicate IDs, keep one clean row (first good row) and remove duplicate resubmissions.
5. Clean `amount_usd`:
   - `Edit cells` -> `Transform...`
   - Use GREL like: `value.replace(/[^0-9.\\-]/,'')`
   - Convert the column to number (`Edit cells` -> `Common transforms` -> `To number`).
6. Filter rows to:
   - `supplier_name = Zenith Components`
   - `category = Facility`
   - `status = Approved`
7. Sum `amount_usd` for the filtered rows.
8. Total Approved spend is **`49143.64` USD**.

## Validation snapshot
- Matching rows after cleaning/filtering: 8
- Total spend: 49143.64
