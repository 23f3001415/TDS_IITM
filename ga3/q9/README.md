# Q9: PDF Text Bounding Box Detection

## ELI15 Step-by-Step (Beginner Friendly)

1. Open terminal in `ga3/q9`.
2. Install PyMuPDF:
   ```powershell
   pip install pymupdf
   ```
3. Run:
   ```powershell
   python main.py "C:\Users\sriva\Downloads\bounding_box_task.pdf" text
   ```
4. Copy the JSON array printed in terminal.
5. Paste that exact JSON in the grader.

## Files

- `main.py`: extracts all bounding boxes for a target word using `page.search_for()`

