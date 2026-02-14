# Q11 - Configure a Codespace DevContainer (ELI15 Guide)

Think of a DevContainer like a "ready-made laptop setup" that GitHub gives you in the cloud.
Instead of installing everything on your own computer, you describe the setup once in a file, and Codespaces builds it for you.

## Goal
You need a repo that has:
- `.devcontainer/devcontainer.json`
- `"name": "ga2-d7b4e0"`
- feature `ghcr.io/devcontainers/features/python:1`
- VS Code extensions `astral-sh.uv` and `ms-python.python`
- post-create command `uv pip install fastapi`

Then you must start a Codespace and run:

```bash
echo $GITHUB_REPOSITORY $GITHUB_TOKEN
```

And paste that output into the assignment.

## Step-by-step (complete novice)
1. Open your GA2 GitHub repository in browser.
2. In the repo root, create a folder named `.devcontainer`.
3. Inside it, create `devcontainer.json`.
4. Paste this exact content:

```json
{
  "name": "ga2-d7b4e0",
  "image": "mcr.microsoft.com/devcontainers/base:ubuntu",
  "features": {
    "ghcr.io/devcontainers/features/python:1": {}
  },
  "customizations": {
    "vscode": {
      "extensions": [
        "astral-sh.uv",
        "ms-python.python"
      ]
    }
  },
  "postCreateCommand": "uv pip install fastapi"
}
```

5. Commit and push these changes to GitHub.
6. Click the green `Code` button in GitHub.
7. Go to `Codespaces` tab.
8. Click `Create codespace on main` (or your assignment branch).
9. Wait for Codespace to build. It can take a few minutes first time.
10. Open the terminal inside Codespace.
11. Run:

```bash
echo $GITHUB_REPOSITORY $GITHUB_TOKEN
```

12. You will see two space-separated values:
- first value: repo slug (example format: `username/repo-name`)
- second value: temporary token for this Codespace session

13. Copy that full line and submit it in the assignment field `Repository slug and token`.

## Common mistakes
- Folder name is wrong (`devcontainer` instead of `.devcontainer`).
- File is not valid JSON (missing comma or quote).
- Codespace was created before adding `devcontainer.json` (rebuild it).
- Token is blank because command was run outside Codespace.

## Safe note
`GITHUB_TOKEN` is secret-like. Use it only for the assignment and do not post publicly outside the submission.

## What I completed locally for you
- Created `.devcontainer/devcontainer.json` with the required config.
- Added this guide file at `q11/ELI15_q11_solution.md`.

What still needs your live GitHub session:
- Launch Codespace.
- Run the `echo` command there.
- Paste exact output into assignment.