# Q7 GitHub Action with Dependency Caching - ELI15 Step-by-Step

1. Create `.github/workflows/q7-cache.yml`.
2. Add `actions/cache@v4` step with key `cache-7aa4fea`.
3. Add step named `prime-cache-7aa4fea` and print cache hit/miss from `steps.<id>.outputs.cache-hit`.
4. Add dependency install step (example: `pip install -r ga2/q7/requirements.txt`).
5. Commit and push workflow.
6. Trigger workflow once (Actions tab or `gh workflow run q7-cache.yml`).
7. Keep repository public and latest run visible for grading.
8. Submit repository URL:
   `https://github.com/23f3001415/TDS_IITM`
