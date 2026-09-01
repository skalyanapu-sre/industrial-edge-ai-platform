# Phase 01 — Repository Baseline

## Goal
Create a clean Git repository, reproducible Python environment, test harness, documentation structure, and first GitHub CI gate. **No Azure resource is created in this phase.**

## Run on your Mac

```bash
cd ~/Desktop/databricks_projects/industrial-edge-ai-platform
git status
python3 --version
git --version
gh --version
az version
terraform version
docker --version
```

Copy the repository skeleton files for this phase: `.gitignore`, `pyproject.toml`, `requirements*.txt`, `Makefile`, `.github/workflows/01-ci.yml`, `docs/`, `scripts/`.

Create the environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -e '.[dev]'
ruff check .
ruff format --check .
pytest -q
```

At this phase the application tests may be present already, but Azure must still be untouched.

## Git gate

```bash
git checkout -b feature/phase-01-repo-baseline
git add .
git diff --cached --check
git status
git commit -m "chore: establish repository quality baseline"
git push -u origin feature/phase-01-repo-baseline
gh pr create --fill
```

GitHub: `Actions -> CI` must be green. Merge only after the checks pass.

After merge:

```bash
git checkout main
git pull --ff-only
git log --oneline -5
```

**Definition of Done:** local lint/tests pass, CI passes, PR merged, main clean.
