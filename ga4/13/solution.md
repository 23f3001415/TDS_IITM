# Question 13: Shell - Extract and Flatten Nested JSON

## Final Answer (submit this)
`level1:56|level2:45|level3:57|level4:47|level5:49|level6:44|level7:50|level8:38|level9:48|level10:40`

## ELI15 Step-by-Step (for a complete novice)
1. Unzip `api_data_23f3001415@ds.study.iitm.ac.in.zip`.
2. Find all `.json` files in the extracted folder.
3. Each file has an array of records.
4. From each record, read nested field `metrics.level`.
5. Collect all level values from all files.
6. Count how many times each level appears (1 to 10).
7. Sort by level number.
8. Print as:
   - `level1:count|level2:count|...|level10:count`

## jq-style command pattern
```sh
find extracted -name "*.json" -print0 \
| xargs -0 jq -r '.[] | .metrics.level' \
| sort -n \
| uniq -c \
| awk '{printf "level%s:%s\n",$2,$1}' \
| sort -t: -k1.6,1n \
| paste -sd'|' -
```

## Validation snapshot
- JSON files processed: 57
- Total records counted: 474
