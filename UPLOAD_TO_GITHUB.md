# Put this repository on GitHub

1. Create an empty GitHub repository named `intercept-analytics-workflow`.
2. In a terminal, open this folder.
3. Run:

```bash
git init
git branch -M main
git add .
git commit -m "Set up analytics workflow demo"
git remote add origin YOUR_GITHUB_REPO_URL
git push -u origin main
```

4. Open the repository's **Actions** tab. The `checks` workflow should run on the push to `main`.
5. After the checks have appeared at least once, create a branch ruleset for `main` under **Settings → Rules → Rulesets**. Require:
   - pull requests before merging;
   - one approving review;
   - the five status checks: `hygiene`, `tests`, `data-contract`, `score-check`, `reproducibility`;
   - the branch to be up to date before merge.

## Create the live-demo pull request

```bash
git switch main
git pull
git switch -c alex/wait-60-days
```

Edit `config/client.yml` from:

```yaml
quiet_days: 30
```

to:

```yaml
quiet_days: 60
```

Then:

```bash
git add config/client.yml
git commit -m "Extend waiting period to 60 days"
git push -u origin alex/wait-60-days
```

Open the pull request in GitHub. CI should report the synthetic accuracy moving from `0.81` to `0.84`.
