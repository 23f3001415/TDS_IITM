# Q4: Create a Scheduled GitHub Action

## ELI15 Step-by-Step (Beginner Friendly)

1. Create a GitHub repository.
2. Inside the repo, create folder `.github/workflows/`.
3. Create file `.github/workflows/daily-commit.yml`.
4. Add a workflow that:
   - runs once daily using cron with fixed minute+hour
   - has one step name containing `23f3001415@ds.study.iitm.ac.in`
   - writes timestamp to a file and commits it
5. Push this workflow to GitHub.
6. Trigger it manually using **Run workflow** (or `gh workflow run`).
7. Wait for completion and confirm:
   - this run is the most recent action
   - a commit was created during or within 5 minutes of the run
8. Submit the repository URL.

## Workflow Used

Path:

`.github/workflows/daily-commit.yml`

Cron used:

`17 4 * * *` (runs daily at 04:17 UTC)

Required email in step name:

`23f3001415@ds.study.iitm.ac.in - Generate daily update`

## Final Answer (for grader)

Repository URL:

`https://github.com/23f3001415/tds-ga3-q4-daily-action`

Latest workflow run:

`https://github.com/23f3001415/tds-ga3-q4-daily-action/actions/runs/22305994073`
