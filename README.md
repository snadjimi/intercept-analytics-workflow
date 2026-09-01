# Analytics on GitHub — Intercept take-home

A small, fully synthetic repository that demonstrates the workflow recommended in the presentation:

**short branch → pull request → automated checks → review → merge → deliverable tag**

No client data is included. The model is intentionally simple so every branch, test, metric and CI failure can be explained live.

## What is here

- `presentation/intercept-workflow-deck.pptx` — presentation deck
- `demo/intercept-workflow-demo.html` — interactive walkthrough
- `.github/workflows/ci.yml` — five CI layers
- `src/` — tiny deterministic analytics pipeline
- `tests/` — business-rule and data-contract tests
- `data/sample/customers.csv` — synthetic labelled sample
- `metrics/baseline.json` — previous-deliverable baseline
- `config/client.yml` — versioned analytical parameters

## The five CI checks

1. **hygiene** — formatting, linting, notebook outputs, oversized files, obvious credentials and hard-coded local paths
2. **tests** — analytical business-rule tests
3. **data-contract** — schema, uniqueness and null-rate assumptions
4. **score-check** — compares the current analytical result with the recorded baseline
5. **reproducibility** — runs the exact evaluation twice and requires byte-identical output

The workflow reports these checks. A GitHub ruleset on `main` is what makes them mandatory before merge.

## Run locally

```bash
python -m pip install -r requirements.txt
ruff format --check .
ruff check .
pytest -q
python -m src.contracts.validate data/sample/customers.csv
python -m src.models.evaluate \
  --customers data/sample/customers.csv \
  --baseline metrics/baseline.json \
  --out metrics/pr.json
```

The committed `main` state uses the **30-day** inactivity threshold and scores **0.81** on the synthetic sample. For the live pull request, change `config/client.yml` to **60 days**; that version scores **0.84**.

## Suggested live PR

Create a branch such as `alex/wait-60-days`, change `quiet_days: 30` to `quiet_days: 60` in `config/client.yml`, push it, and open a pull request. The PR template asks the author to state:

- what changed and why;
- what number moved;
- how it was checked;
- what was not checked.

For a deliberate red CI run, change the null handling in `src/features.py` or set an obviously poor `quiet_days` value, push again, and show that the same PR reruns automatically.
