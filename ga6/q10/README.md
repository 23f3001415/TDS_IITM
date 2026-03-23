# Q10: The Leakage Auditor

## ELI15 Step-by-Step (Complete Beginner)

1. You have two files:
   - `questions.csv`
   - `corpus.txt`
2. The idea is to check whether a benchmark question looks copied from the corpus.
3. We do that using **8-grams**.
4. An 8-gram means:
   - take 8 words in a row
   - join them as one chunk
5. Example:
   - tokens = `["a","b","c","d","e","f","g","h","i"]`
   - 8-grams are:
   - `"a b c d e f g h"`
   - `"b c d e f g h i"`
6. First, tokenize text exactly as instructed:
   - lowercase everything
   - replace non-alphanumeric characters with spaces
   - split on whitespace
   - remove empty tokens
7. Build **all** 8-grams from `corpus.txt` once.
8. Store them in a Python `set`.
9. A set makes lookup very fast.
10. For each question:
   - tokenize it
   - generate its 8-grams
   - count how many of those 8-grams also appear in the corpus set
11. Then compute:
   - `overlap_score = hits / total_question_8grams`
12. If a question has fewer than 8 tokens:
   - its overlap score is `0`
13. A question is contaminated if:
   - `overlap_score > 0.5`
14. Now compute the 3 required outputs:
   - `contaminated_count`
   - `reported_accuracy`
   - `adjusted_accuracy`
15. `reported_accuracy` uses **all 60 questions**.
16. `adjusted_accuracy` uses only the **non-contaminated** questions.
17. The exact calculation on your downloaded files gives:
   - contaminated questions = `6`
   - reported accuracy = `86.67`
   - adjusted accuracy = `87.04`
18. One interesting detail:
   - the prompt text says adjusted accuracy will always be lower
   - but this seeded file actually gives a slightly higher adjusted accuracy
   - the submitted answer should still follow the computed data, not the narrative hint

## Files in This Folder

- `questions.csv`: copied from your Downloads folder
- `corpus.txt`: copied from your Downloads folder
- `solution.py`: contamination audit script
- `answer.txt`: final submission string

## Run

```powershell
cd C:\Users\sriva\OneDrive\Documents\TDS\ga6\q10
python solution.py
```

## Final Answer To Submit

```text
6,86.67,87.04
```
