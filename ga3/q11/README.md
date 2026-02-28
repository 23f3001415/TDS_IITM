# Q11: AI Video Attendee Extraction

## ELI15 Step-by-Step

1. In the assignment page, click **Generate & Record Video**.
2. Keep that tab active for the full recording (~44 seconds).
3. Wait until the counter reaches **`20/20`** before downloading.
4. Save the file as `.webm` (for example in `Downloads`).
5. Open PowerShell in this folder (`ga3/q11`).
6. Install dependency:
   ```powershell
   pip install google-genai
   ```
7. Set API key in the same terminal:
   ```powershell
   $env:GEMINI_API_KEY="your_real_key_here"
   ```
8. Run extractor:
   ```powershell
   python main.py "C:\Users\sriva\Downloads\attendee_checkin.webm"
   ```
9. Copy the JSON array printed by the script.
10. Paste into grader and submit.

## Why 1/20 Happens

- Your video is incomplete or frozen (common symptom: `CHECKED IN: 1 / 20` stays on screen).
- In that case, regenerate the video and keep the tab focused until recording ends.
