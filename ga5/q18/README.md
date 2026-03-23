# Q18: Local RAG with `llm` CLI

## ELI15 Step-by-Step (Complete Beginner)

1. Put `company_policies.md` in your working folder.
2. Install the tool:
   `pip install llm`
3. (Optional) add an embedding plugin/model you want to use.
4. Embed the handbook into a local collection:

```powershell
llm embed-multi policies `
  -m 3-small `
  --files . "company_policies.md" `
  --store
```

5. Ask your exact question:

```powershell
llm similar policies -c "How many days per week are employees permitted to work remotely under the hybrid work policy?"
```

6. Open the top matching paragraph and read the integer mentioned explicitly.
7. The paragraph says employees may work remotely up to **2 days per week**.
8. Submit only the integer.

## Files in This Folder

- `company_policies.md`: handbook
- `solution.py`: direct extractor for the same integer
- `answer.txt`: final integer answer

## Final Answer

`2`

