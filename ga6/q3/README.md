# Q3: The Multi-Model Robustness Audit

## ELI15 Step-by-Step (Complete Beginner)

1. You have 21 instruction fragments, each with:
   - a word count
   - one score contribution per model
2. You also have pair bonuses.
3. If two specific fragments are chosen together, that pair bonus is added too.
4. The tricky part is the bottom line:
   - `gpt-4o: -2.37`
   - `gpt-4.1: -0.68`
   - `gpt-4.1-mini: -2.48`
   - `gpt-5-mini: 0.03`
5. These are **not** percentages directly.
6. They act like **logits**.
7. So the correct scoring method is:
   - add base logit
   - add selected fragment logits
   - add pair bonuses
   - convert each final logit to a percentage with the sigmoid formula
8. The conversion is:
   - `percent = 100 / (1 + exp(-logit))`
9. After that:
   - `Macro-Mean` = average of the 4 model percentages
   - `Model Floor` = smallest of the 4 model percentages
10. Your goal is the **shortest** combination whose:
   - Macro-Mean is at least `97`
   - Model Floor is at least `92`
11. There are `2^21 = 2,097,152` possible combinations.
12. That is still small enough to solve exactly.
13. I used a meet-in-the-middle search:
   - split the 21 fragments into 2 halves
   - enumerate all subsets in each half
   - combine them efficiently with the cross-pair bonuses
14. Under the correct logit-space scoring model, the unique shortest solution is:
   - `I1, I11, I14, I15, I17, I19`
15. Its total word count is:
   - `9 + 8 + 12 + 10 + 5 + 16 = 60`
16. The active pair bonuses are:
   - `I1,I11 = +0.59`
   - `I1,I19 = +0.45`
   - total pair bonus = `+1.04`
17. Final logits become:
   - `gpt-4o = 4.05`
   - `gpt-4.1 = 5.80`
   - `gpt-4.1-mini = 3.76`
   - `gpt-5-mini = 2.60`
18. Converting those logits to percentages gives:
   - `gpt-4o = 98.29%`
   - `gpt-4.1 = 99.70%`
   - `gpt-4.1-mini = 97.72%`
   - `gpt-5-mini = 93.09%`
19. So:
   - `Macro-Mean = 97.20%`
   - `Model Floor = 93.09%`
20. That passes both thresholds, and no shorter combination does.

## Final Answer To Submit

```text
I1,I11,I14,I15,I17,I19;60;97.20%;93.09%
```

## Files in This Folder

- `solution.py`: exact logit-space solver
- `answer.txt`: final submission string

Run:

```powershell
cd C:\Users\sriva\OneDrive\Documents\TDS\ga6\q3
python solution.py
```
