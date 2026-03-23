# Q14: The Benchmark Overfitter

## ELI15 Step-by-Step

1. First compute `sigma` using:
   - `sqrt(p * (1 - p) / n_test)`
2. Here:
   - `p = 0.94`
   - `n_test = 2000`
3. Then compute expected inflation:
   - `sigma * sqrt(2 * ln(T))`
4. Here:
   - `T = 50`
5. Convert inflation to percentage points by multiplying by `100`.
6. Then subtract it from the reported `94.000%`.

## Final Answer

```text
0.005310,1.485,92.515
```
