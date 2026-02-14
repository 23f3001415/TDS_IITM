# Q3 Git Time Travel - ELI15 Step-by-Step

Think of Git like a time machine for your project.
You need to find:
1) The commit where `timeout` became `900`
2) The parent (one step before it)
3) Submit the parent's **7-character short hash**

## 1) Go inside the extracted repo
In PowerShell:

```powershell
cd "c:\Users\sriva\OneDrive\Documents\TDS\ga2\q3\run_20260214_093720\q-git-time-travel"
```

## 2) See history for `config.json`

```powershell
git log --oneline -- config.json
```

This shows commits that touched `config.json`.

## 3) Narrow to timeout-related changes

```powershell
git log --oneline -S "900" -- config.json
```

This finds commits where `900` appeared/disappeared.

## 4) Inspect the key commit

```powershell
git show eff3987 -- config.json
```

You can see this commit changed:
- `"timeout": 90` -> `"timeout": 900`

So commit `eff3987` is the one that set timeout to 900.

## 5) Find its parent commit

```powershell
git rev-parse --short=7 eff3987^
```

Output:

```text
cb000a8
```

## Final answer to submit
`cb000a8`
