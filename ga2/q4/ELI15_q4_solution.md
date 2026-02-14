# Q4 Host Portfolio on GitHub Pages - ELI15 Step-by-Step

Goal: Publish a simple portfolio page and include your IITM email in HTML with special wrappers.

## 1) Create your page file
Create `index.html` in your repo (root is easiest for GitHub Pages).

## 2) Add your portfolio content
Keep it simple: your name, projects, and contact section.

## 3) Add email exactly like this
```html
<!--email_off-->23f3001415@ds.study.iitm.ac.in<!--/email_off-->
```
Do not change spelling or wrapper comments.

## 4) Commit and push
```powershell
git add index.html
git commit -m "Add portfolio page for GitHub Pages"
git push
```

## 5) Enable GitHub Pages
On GitHub:
1. Open repo `TDS_IITM`
2. Go to `Settings` -> `Pages`
3. Under Build and deployment:
   - Source: `Deploy from a branch`
   - Branch: `main`
   - Folder: `/ (root)`
4. Click `Save`

## 6) Wait 1-2 minutes and open URL
Expected URL:
`https://23f3001415.github.io/TDS_IITM/`

If not updated, try:
- `https://23f3001415.github.io/TDS_IITM/?v=1`
- `https://23f3001415.github.io/TDS_IITM/?v=2`

## Final answer format
Submit this GitHub Pages URL:
`https://23f3001415.github.io/TDS_IITM/`
