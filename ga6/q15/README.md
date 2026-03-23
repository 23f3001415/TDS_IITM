# Q15: The Coverage Gap Finder

## ELI15 Step-by-Step

1. Line coverage is:
   - `executed_lines / total_statements * 100`
2. Branch coverage is:
   - `number_of_true_branches / total_branches * 100`
3. Sort the missing lines.
4. Group consecutive integers into blocks.
5. Each test can cover at most `4` consecutive missing lines.
6. So for each block, needed tests are:
   - `ceil(block_size / 4)`
7. Add those values to get `missing_line_runs`.
8. The largest block size is `critical_missing`.

## Final Answer

```text
65.00,46.00,17,7
```
