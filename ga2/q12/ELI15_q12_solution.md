# Q12 - Host a File on GitHub Gist (ELI15 Guide)

Think of GitHub Gist like posting a single file on the internet with its own link.
For this question, your file must include your IITM email in HTML so the checker can find it.

## What you must submit
- One GitHub Gist URL in this format:
  - `https://gist.github.com/<username>/<gist_id>`

## Step-by-step for a complete beginner
1. Open `https://gist.github.com/` and sign in to GitHub.
2. In the filename box, type `gist_showcase.html`.
3. Paste this HTML (contains your email in visible text + metadata + comment):

```html
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>GA2 Q12 Showcase</title>
  <meta name="author-email" content="23f3001415@ds.study.iitm.ac.in">
</head>
<body>
  <h1>GA2 Q12 Showcase</h1>
  <p>This file is published on GitHub Gist for assignment verification.</p>
  <p>Email for verification: 23f3001415@ds.study.iitm.ac.in</p>
  <!-- verification-email:23f3001415@ds.study.iitm.ac.in -->
</body>
</html>
```

4. Click `Create public gist`.
5. Copy the Gist URL from browser address bar.
6. Submit that URL in the answer box.

## Why this works even with obfuscation
- Some pages hide emails when rendered.
- Here the email is included in multiple HTML locations (`meta`, visible text, HTML comment), so it still appears in page HTML for verification.

## Cache tip from assignment
If a recent edit is not visible, try:
- `?v=1`
- `?v=2`
Example: `https://gist.github.com/23f3001415/643c2a13b1f1b70da4c039eabc9079fe?v=1`

## Final answer for this question
`https://gist.github.com/23f3001415/643c2a13b1f1b70da4c039eabc9079fe`