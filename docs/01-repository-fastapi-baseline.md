# Phase 01 — Repository & FastAPI Edge Inference Baseline

> **Project:** Industrial Edge AI Platform
> **Phase:** 01
> **Scope:** Local application baseline, telemetry simulation, automated testing, Git lifecycle, GitHub Actions CI, merge, and post-merge validation
> **Azure resources created:** None
> **Terraform used:** No

---

## 1. Objective

Phase 01 establishes the first independently runnable component of the Industrial Edge AI Platform.

The purpose of this phase is to prove that a clean checkout of the repository contains everything required to:

1. create a Python environment;
2. install the project;
3. start a FastAPI inference service;
4. validate industrial telemetry using Pydantic;
5. replay synthetic HVAC telemetry;
6. return explainable risk predictions;
7. expose Prometheus metrics;
8. run automated tests and code-quality checks;
9. commit the change on a feature branch;
10. validate it in GitHub Actions;
11. merge it into `main`;
12. revalidate the merged code.

No Azure, Terraform, Databricks, AKS, IoT Hub, or NVIDIA Jetson work belongs in this phase.

---

## 2. Engineering Lifecycle Used in Every Phase

```text
CREATE
  ↓
TEST LOCALLY
  ↓
VALIDATE OUTPUT
  ↓
REVIEW GIT DIFF
  ↓
COMMIT
  ↓
PUSH FEATURE BRANCH
  ↓
PULL REQUEST
  ↓
CI VALIDATION
  ↓
MERGE
  ↓
POST-MERGE VALIDATION
  ↓
PHASE CLOSED
```

A phase is **not complete because code exists**. It is complete only after the code is reproducible, tested, reviewed, merged, and revalidated from `main`.

---

## 3. Phase 01 Architecture

```text
Synthetic HVAC CSV
       │
       ▼
simulator/replay.py
       │
       │ HTTP POST /v1/predict
       ▼
     FastAPI
       │
       ▼
Pydantic Validation
       │
       ▼
Predictor Interface
       │
       ▼
RuleBasedPredictor
       │
       ├──────────────► JSON Prediction
       │
       └──────────────► Prometheus Metrics (/metrics)
```

Later phases will replace parts of this flow without changing the basic API contract:

```text
CSV simulator       → IoT Hub / Event Hubs / industrial protocols
RuleBasedPredictor  → ONNX / MLflow-approved model
Mac CPU             → Docker / AKS / IoT Edge / Jetson
```

---

## 4. Definition of Done

Phase 01 is complete only when all items are true:

```text
[ ] Feature branch created from clean main
[ ] Repository structure created
[ ] Python 3.12 virtual environment created
[ ] Editable installation succeeds
[ ] FastAPI starts successfully
[ ] GET /health returns HTTP 200
[ ] GET /ready returns HTTP 200
[ ] POST /v1/predict returns a prediction
[ ] Invalid telemetry is rejected with HTTP 422
[ ] GET /metrics exposes Prometheus metrics
[ ] Sample telemetry CSV exists
[ ] Simulator successfully replays telemetry
[ ] Healthy reading returns normal severity
[ ] Abnormal reading exercises critical severity
[ ] Ruff lint passes
[ ] Ruff formatting check passes
[ ] Pytest passes
[ ] Git whitespace validation passes
[ ] Secrets/generated files are excluded from Git
[ ] Feature branch committed and pushed
[ ] Pull Request created
[ ] GitHub Actions CI passes
[ ] Pull Request merged to main
[ ] main pulled locally
[ ] Tests pass again from main
[ ] GitHub Actions passes on main
```

---

# 5. Start From the Existing Repository

## Where

Mac Terminal.

```bash
cd ~/Desktop/databricks_projects/industrial-edge-ai-platform
```

Verify:

```bash
pwd
git status
git branch --show-current
git remote -v
```

Expected repository path pattern:

```text
/Users/<username>/Desktop/databricks_projects/industrial-edge-ai-platform
```

---

# 6. Synchronize `main`

```bash
git checkout main
git pull --ff-only
git status
```

Target:

```text
On branch main
nothing to commit, working tree clean
```

Why: every phase starts from a known-good integration branch.

---

# 7. Create the Phase 01 Feature Branch

```bash
git checkout -b feature/phase-01-fastapi-baseline
```

Verify:

```bash
git branch --show-current
```

Expected:

```text
feature/phase-01-fastapi-baseline
```

---

# 8. Create the Directory Structure

```bash
mkdir -p \
  app/api \
  app/models \
  app/services \
  app/observability \
  simulator \
  data/sample \
  tests \
  docs/phases \
  .github/workflows
```

Create Python package markers:

```bash
touch \
  app/__init__.py \
  app/api/__init__.py \
  app/models/__init__.py \
  app/services/__init__.py \
  app/observability/__init__.py \
  simulator/__init__.py
```

Result:

```text
industrial-edge-ai-platform/
├── .github/
│   └── workflows/
├── app/
│   ├── api/
│   ├── models/
│   ├── observability/
│   └── services/
├── data/
│   └── sample/
├── docs/
│   └── phases/
├── simulator/
└── tests/
```

---

# 9. Create `.gitignore`

Create or edit `.gitignore`:

```gitignore
# Python
__pycache__/
*.py[cod]
*.pyo
*.pyd
*.egg-info/

# Virtual environments
.venv/
venv/

# Test / tool caches
.pytest_cache/
.ruff_cache/
.coverage
htmlcov/

# Environment / secrets
.env
.env.local
.env.*.local
!.env.example

# Terraform - used in future phases
**/.terraform/*
*.tfstate
*.tfstate.*
*.tfplan
*.tfvars
*.tfvars.json
!*.tfvars.example
crash.log
crash.*.log

# macOS
.DS_Store

# IDE
.vscode/
.idea/

# ML artifacts
*.onnx
*.pkl
*.joblib
```

### Why

Do not commit local environments, generated metadata, state files, secrets, IDE data, or generated model artifacts.

---

# 10. Optional `.python-version`

If using `pyenv`, commit a project Python version file:

```bash
echo "3.12.14" > .python-version
cat .python-version
```

This gives developers a predictable local Python version when `pyenv` is installed.

---

# 11. Create `pyproject.toml`

```toml
[build-system]
requires = ["setuptools>=75", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "industrial-edge-ai-platform"
version = "0.1.0"
description = "Industrial Edge AI predictive maintenance reference platform"
requires-python = ">=3.12,<3.14"
dependencies = [
    "fastapi>=0.116,<1.0",
    "uvicorn[standard]>=0.35,<1.0",
    "prometheus-client>=0.22,<1.0",
    "httpx>=0.28,<1.0"
]

[project.optional-dependencies]
dev = [
    "pytest>=8,<9",
    "ruff>=0.12,<1.0"
]

[tool.setuptools.packages.find]
where = ["."]
include = ["app", "app.*"]
exclude = [
    "data",
    "data.*",
    "simulator",
    "simulator.*",
    "tests",
    "tests.*",
    "docs",
    "docs.*",
    "infra",
    "infra.*"
]
namespaces = false

[tool.pytest.ini_options]
testpaths = ["tests"]
pythonpath = ["."]

[tool.ruff]
line-length = 100
target-version = "py312"

[tool.ruff.lint]
select = ["E", "F", "I", "B", "UP"]
```

## Why explicit package discovery matters

The repository is intentionally multi-purpose:

```text
app/         production Python package
data/        sample data
simulator/   engineering utility
tests/       automated tests
docs/        documentation
infra/       future Terraform
```

Only `app/` should be packaged as the production Python application. Explicit discovery prevents `setuptools` from guessing incorrectly.

---

# 12. Create and Activate the Virtual Environment

```bash
python3 --version
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
```

The prompt should show something similar to:

```text
(.venv)
```

It is safe to run Git commands while `.venv` is active. The virtual environment affects Python-related commands, not Git.

---

# 13. Install the Project

```bash
pip install -e '.[dev]'
```

`-e` means editable install: code changes in the repository are immediately visible to the installed project.

Validate:

```bash
pip show industrial-edge-ai-platform
python -c "import app; print(app.__file__)"
```

---

# 14. Create the Telemetry Schema

File: `app/models/schemas.py`

```python
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class SensorReading(BaseModel):
    model_config = ConfigDict(extra="forbid")

    asset_id: str = Field(min_length=1, max_length=128)
    timestamp: datetime
    temperature_f: float = Field(ge=-40, le=250)
    humidity_pct: float = Field(ge=0, le=100)
    co2_ppm: float = Field(ge=0, le=100_000)
    vibration_mm_s: float = Field(ge=0, le=100)
    power_kw: float = Field(ge=0, le=10_000)
    supply_air_temp_f: float = Field(ge=-40, le=250)
    return_air_temp_f: float = Field(ge=-40, le=250)
    fan_speed_pct: float = Field(ge=0, le=100)


class Prediction(BaseModel):
    asset_id: str
    risk_score: float = Field(ge=0, le=1)
    severity: Literal["normal", "watch", "critical"]
    predicted_failure_mode: str
    reasons: list[str]
    model_backend: str
    model_version: str
```

### Logic

The API receives untrusted JSON. Pydantic converts it into a validated domain object before prediction logic executes.

Example:

```text
humidity_pct = 46   → valid
humidity_pct = 150  → HTTP 422
```

`extra="forbid"` prevents silent schema drift caused by unexpected fields.

---

# 15. Create the Predictor Contract

File: `app/services/base.py`

```python
from abc import ABC, abstractmethod

from app.models.schemas import Prediction, SensorReading


class Predictor(ABC):
    @abstractmethod
    def predict(self, reading: SensorReading) -> Prediction:
        raise NotImplementedError
```

### Why

The HTTP layer should not be tightly coupled to one model implementation.

```text
FastAPI → Predictor → RuleBasedPredictor
```

Later:

```text
FastAPI → Predictor → ONNXPredictor
```

---

# 16. Create the Demonstration Predictor

File: `app/services/rules_predictor.py`

```python
from app.models.schemas import Prediction, SensorReading
from app.services.base import Predictor


class RuleBasedPredictor(Predictor):
    backend_name = "explainable-hvac-risk"
    version = "demo-rules-1.0"

    def predict(self, reading: SensorReading) -> Prediction:
        risk = 0.0
        reasons: list[str] = []

        temperature_delta = reading.return_air_temp_f - reading.supply_air_temp_f

        if reading.vibration_mm_s >= 7:
            risk += 0.40
            reasons.append("Very high vibration may indicate bearing or fan imbalance.")
        elif reading.vibration_mm_s >= 5:
            risk += 0.25
            reasons.append("Elevated vibration requires inspection.")

        if reading.fan_speed_pct >= 85 and temperature_delta < 10:
            risk += 0.25
            reasons.append(
                "Low return-to-supply temperature differential while fan speed is high."
            )

        if reading.power_kw >= 18:
            risk += 0.15
            reasons.append("Power draw is above the demo operating threshold.")

        if reading.co2_ppm >= 1200:
            risk += 0.10
            reasons.append("CO2 is elevated and may indicate ventilation deficiency.")

        if reading.temperature_f >= 85:
            risk += 0.10
            reasons.append("Equipment-area temperature is elevated.")

        risk = min(risk, 1.0)

        if risk >= 0.70:
            severity = "critical"
        elif risk >= 0.30:
            severity = "watch"
        else:
            severity = "normal"

        if reading.vibration_mm_s >= 5:
            failure_mode = "mechanical_degradation"
        elif reading.fan_speed_pct >= 85 and temperature_delta < 10:
            failure_mode = "cooling_efficiency_degradation"
        else:
            failure_mode = "no_anomaly"

        if not reasons:
            reasons.append("Sensor values are within the demo operating envelope.")

        return Prediction(
            asset_id=reading.asset_id,
            risk_score=round(risk, 2),
            severity=severity,
            predicted_failure_mode=failure_mode,
            reasons=reasons,
            model_backend=self.backend_name,
            model_version=self.version,
        )
```

> **Important:** These thresholds are demonstration logic. They are not OEM limits or a validated production HVAC failure model.

---

# 17. Create Prometheus Metrics

File: `app/observability/metrics.py`

```python
from prometheus_client import Counter, Histogram


INFERENCE_REQUESTS = Counter(
    "edgeai_inference_requests_total",
    "Total number of inference requests.",
)

INFERENCE_PREDICTIONS = Counter(
    "edgeai_predictions_total",
    "Predictions grouped by severity.",
    ["severity"],
)

INFERENCE_DURATION = Histogram(
    "edgeai_inference_duration_seconds",
    "Time spent performing inference.",
)
```

These metrics establish the observability contract used in later SRE phases.

---

# 18. Create API Routes

File: `app/api/routes.py`

```python
from time import perf_counter

from fastapi import APIRouter, Response
from prometheus_client import CONTENT_TYPE_LATEST, generate_latest

from app.models.schemas import Prediction, SensorReading
from app.observability.metrics import (
    INFERENCE_DURATION,
    INFERENCE_PREDICTIONS,
    INFERENCE_REQUESTS,
)
from app.services.rules_predictor import RuleBasedPredictor


router = APIRouter()
predictor = RuleBasedPredictor()


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@router.get("/ready")
def ready() -> dict[str, str]:
    return {
        "status": "ready",
        "model_backend": predictor.backend_name,
        "model_version": predictor.version,
    }


@router.get("/model")
def model_info() -> dict[str, str]:
    return {
        "backend": predictor.backend_name,
        "version": predictor.version,
    }


@router.post("/v1/predict", response_model=Prediction)
def predict(reading: SensorReading) -> Prediction:
    INFERENCE_REQUESTS.inc()

    started = perf_counter()
    prediction = predictor.predict(reading)
    elapsed = perf_counter() - started

    INFERENCE_DURATION.observe(elapsed)
    INFERENCE_PREDICTIONS.labels(severity=prediction.severity).inc()

    return prediction


@router.get("/metrics")
def metrics() -> Response:
    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST,
    )
```

### Endpoint responsibilities

| Endpoint | Purpose |
|---|---|
| `/health` | Process is alive |
| `/ready` | Service is ready to handle inference |
| `/model` | Current predictor identity/version |
| `/v1/predict` | Validate telemetry and return prediction |
| `/metrics` | Prometheus metrics |

---

# 19. Create the FastAPI Application

File: `app/main.py`

```python
from fastapi import FastAPI

from app.api.routes import router


app = FastAPI(
    title="Industrial Edge AI Inference API",
    description=(
        "Reference API for industrial telemetry validation "
        "and predictive-maintenance inference."
    ),
    version="0.1.0",
)

app.include_router(router)


@app.get("/")
def root() -> dict[str, str]:
    return {
        "service": "industrial-edge-ai-platform",
        "docs": "/docs",
    }
```

`main.py` creates the application; route and inference logic remain in separate modules.

---

# 20. Create Sample Telemetry

File: `data/sample/hvac_sensor_readings.csv`

```csv
asset_id,timestamp,temperature_f,humidity_pct,co2_ppm,vibration_mm_s,power_kw,supply_air_temp_f,return_air_temp_f,fan_speed_pct
AHU-ATL-01,2026-09-01T12:00:00Z,74.2,46,710,2.1,11.4,55,73,62
AHU-ATL-01,2026-09-01T12:05:00Z,74.5,47,725,2.3,11.8,55,73.5,64
AHU-ATL-02,2026-09-01T12:10:00Z,78.0,51,820,3.8,14.2,58,74,76
AHU-ATL-02,2026-09-01T12:15:00Z,80.0,54,980,4.7,16.2,61,75,84
AHU-ATL-02,2026-09-01T12:20:00Z,84.0,57,1180,5.6,18.1,64,75,88
AHU-ATL-02,2026-09-01T12:25:00Z,89.0,59,1450,8.2,21.5,67,72,92
```

The values are synthetic and intentionally progress from healthy to abnormal conditions.

---

# 21. Create the Simulator

File: `simulator/replay.py`

```python
import argparse
import csv
import time
from pathlib import Path

import httpx


DEFAULT_DATA_FILE = Path("data/sample/hvac_sensor_readings.csv")


def row_to_payload(row: dict[str, str]) -> dict[str, str | float]:
    return {
        "asset_id": row["asset_id"],
        "timestamp": row["timestamp"],
        "temperature_f": float(row["temperature_f"]),
        "humidity_pct": float(row["humidity_pct"]),
        "co2_ppm": float(row["co2_ppm"]),
        "vibration_mm_s": float(row["vibration_mm_s"]),
        "power_kw": float(row["power_kw"]),
        "supply_air_temp_f": float(row["supply_air_temp_f"]),
        "return_air_temp_f": float(row["return_air_temp_f"]),
        "fan_speed_pct": float(row["fan_speed_pct"]),
    }


def replay(api_url: str, data_file: Path, interval: float) -> None:
    with data_file.open("r", encoding="utf-8", newline="") as file_handle:
        reader = csv.DictReader(file_handle)

        with httpx.Client(timeout=10.0) as client:
            for row in reader:
                payload = row_to_payload(row)

                response = client.post(
                    f"{api_url}/v1/predict",
                    json=payload,
                )
                response.raise_for_status()

                prediction = response.json()

                print(
                    f"{prediction['asset_id']} "
                    f"severity={prediction['severity']} "
                    f"risk={prediction['risk_score']}"
                )

                time.sleep(interval)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--api-url", default="http://127.0.0.1:8000")
    parser.add_argument("--data-file", type=Path, default=DEFAULT_DATA_FILE)
    parser.add_argument("--interval", type=float, default=0.5)
    args = parser.parse_args()

    replay(
        api_url=args.api_url,
        data_file=args.data_file,
        interval=args.interval,
    )


if __name__ == "__main__":
    main()
```

---

# 22. Start and Validate the API

Use two terminals.

## Terminal 1 — API server

```bash
cd ~/Desktop/databricks_projects/industrial-edge-ai-platform
source .venv/bin/activate

uvicorn app.main:app \
  --reload \
  --host 127.0.0.1 \
  --port 8000
```

Expected:

```text
Uvicorn running on http://127.0.0.1:8000
```

Keep Terminal 1 running.

## Terminal 2 — validation

```bash
cd ~/Desktop/databricks_projects/industrial-edge-ai-platform
source .venv/bin/activate
```

Health:

```bash
curl http://127.0.0.1:8000/health
```

Expected:

```json
{"status":"ok"}
```

Readiness:

```bash
curl http://127.0.0.1:8000/ready
```

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

---

# 23. Replay Sensor Data

From Terminal 2:

```bash
python simulator/replay.py --interval 0.5
```

Expected pattern:

```text
AHU-ATL-01 severity=normal risk=0.0
AHU-ATL-01 severity=normal risk=0.0
...
AHU-ATL-02 severity=critical risk=1.0
```

Then validate metrics:

```bash
curl -s http://127.0.0.1:8000/metrics | grep edgeai_
```

Expected metric families:

```text
edgeai_inference_requests_total
edgeai_predictions_total
edgeai_inference_duration_seconds
```

---

# 24. Create Automated Tests

File: `tests/test_api.py`

```python
from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)

HEALTHY_PAYLOAD = {
    "asset_id": "AHU-ATL-01",
    "timestamp": "2026-09-01T12:00:00Z",
    "temperature_f": 74.2,
    "humidity_pct": 46,
    "co2_ppm": 710,
    "vibration_mm_s": 2.1,
    "power_kw": 11.4,
    "supply_air_temp_f": 55,
    "return_air_temp_f": 73,
    "fan_speed_pct": 62,
}

CRITICAL_PAYLOAD = {
    "asset_id": "AHU-ATL-02",
    "timestamp": "2026-09-01T12:25:00Z",
    "temperature_f": 89,
    "humidity_pct": 59,
    "co2_ppm": 1450,
    "vibration_mm_s": 8.2,
    "power_kw": 21.5,
    "supply_air_temp_f": 67,
    "return_air_temp_f": 72,
    "fan_speed_pct": 92,
}


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_healthy_prediction() -> None:
    response = client.post("/v1/predict", json=HEALTHY_PAYLOAD)
    assert response.status_code == 200
    body = response.json()
    assert body["severity"] == "normal"
    assert body["risk_score"] == 0.0


def test_critical_prediction() -> None:
    response = client.post("/v1/predict", json=CRITICAL_PAYLOAD)
    assert response.status_code == 200
    body = response.json()
    assert body["severity"] == "critical"
    assert body["risk_score"] == 1.0


def test_invalid_humidity_is_rejected() -> None:
    payload = HEALTHY_PAYLOAD.copy()
    payload["humidity_pct"] = 150
    response = client.post("/v1/predict", json=payload)
    assert response.status_code == 422


def test_metrics_endpoint() -> None:
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "edgeai_inference_requests_total" in response.text
```

Run:

```bash
pytest -q
```

Observed successful result during Phase 01:

```text
.....
5 passed
```

---

# 25. Code Quality Gate

Format:

```bash
ruff format .
```

Lint:

```bash
ruff check .
```

Validate formatting:

```bash
ruff format --check .
```

Run tests again:

```bash
pytest -q
```

Final local quality gate:

```bash
ruff check .
ruff format --check .
pytest -q
git diff --check
```

---

# 26. GitHub Actions CI

File: `.github/workflows/01-ci.yml`

```yaml
name: 01 - Python CI

on:
  pull_request:
    branches:
      - main

  push:
    branches:
      - main

permissions:
  contents: read

jobs:
  validate-python:
    name: Validate Python
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"
          cache: pip

      - name: Upgrade pip
        run: python -m pip install --upgrade pip

      - name: Install project
        run: pip install -e '.[dev]'

      - name: Ruff lint
        run: ruff check .

      - name: Ruff format check
        run: ruff format --check .

      - name: Run tests
        run: pytest -q
```

## What GitHub creates

`runs-on: ubuntu-latest` requests a temporary GitHub-hosted Linux runner.

```text
Pull Request
     ↓
GitHub Actions
     ↓
Temporary Ubuntu runner
     ↓
Checkout repository
     ↓
Python 3.12
     ↓
Install dependencies
     ↓
Ruff
     ↓
Pytest
     ↓
PASS / FAIL
     ↓
Runner discarded
```

This runner is **not** created in the project's Azure subscription.

---

# 27. Errors Encountered During Phase 01

This section records the real implementation issues encountered and how they were diagnosed.

## 27.1 `pip install -e '.[dev]'` — Multiple Top-Level Packages

### Error

```text
error: Multiple top-level packages discovered in a flat-layout:
['app', 'data', 'simulator'].
```

### Root cause

`setuptools` discovered multiple top-level directories and refused to guess which directories should be installed as Python packages.

### Fix

Add explicit discovery to `pyproject.toml`:

```toml
[tool.setuptools.packages.find]
where = ["."]
include = ["app", "app.*"]
exclude = [
    "data",
    "data.*",
    "simulator",
    "simulator.*",
    "tests",
    "tests.*",
    "docs",
    "docs.*",
    "infra",
    "infra.*"
]
namespaces = false
```

Clean generated metadata:

```bash
rm -rf build dist *.egg-info
```

Retry:

```bash
pip install -e '.[dev]'
```

Validate:

```bash
pip show industrial-edge-ai-platform
python -c "from app.main import app; print(app.title)"
```

### Lesson

Production repositories containing code, data, tests, documentation, and infrastructure should use explicit Python package-discovery rules.

---

## 27.2 `industrial_edge_ai_platform.egg-info/` Appeared as Untracked

### Symptom

`git status` showed:

```text
industrial_edge_ai_platform.egg-info/
```

### Root cause

Editable installation generated Python package metadata.

### Fix

Add to `.gitignore`:

```gitignore
*.egg-info/
```

Remove existing generated metadata:

```bash
rm -rf industrial_edge_ai_platform.egg-info
```

Validate:

```bash
git status
```

The directory should no longer appear.

---

## 27.3 Simulator — `Connection refused`

### Error

```text
httpx.ConnectError: [Errno 61] Connection refused
```

### Root cause

`simulator/replay.py` attempted to send a request to:

```text
http://127.0.0.1:8000/v1/predict
```

but no process was accepting connections on that port.

### Fix

Start FastAPI first:

```bash
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Validate the service before replaying data:

```bash
curl http://127.0.0.1:8000/health
```

Only when health succeeds:

```bash
python simulator/replay.py --interval 0.5
```

### Lesson

Always validate the server dependency before debugging the client.

---

## 27.4 Uvicorn — `Address already in use`

### Error

```text
ERROR: [Errno 48] Address already in use
```

### Root cause

Another process was already listening on TCP port 8000. In this implementation, an existing Uvicorn process was the likely cause.

### Diagnose

```bash
lsof -iTCP:8000 -sTCP:LISTEN
```

Then test the service:

```bash
curl http://127.0.0.1:8000/health
```

If health returns:

```json
{"status":"ok"}
```

reuse the existing server. Do not start a second copy.

If the listener is stale or unrelated:

```bash
ps -fp <PID>
kill <PID>
```

Confirm the port is free:

```bash
lsof -iTCP:8000 -sTCP:LISTEN
```

Then restart Uvicorn.

### Lesson

`Address already in use` is a process/port-ownership problem, not normally an application-code problem.

---

## 27.5 Pytest — Five Tests Passed With One Deprecation Warning

### Observed result

```text
5 passed, 1 warning
```

The warning referenced the FastAPI/Starlette test-client HTTP dependency stack.

### Interpretation

The test assertions passed. The warning is a compatibility/deprecation signal, not a failed test.

### Investigation commands

```bash
pip show fastapi
pip show starlette
pip show httpx
```

If dependency changes are made, rerun:

```bash
pip install -e '.[dev]'
pytest -q
```

### Production rule

Do not blindly suppress dependency warnings. First identify whether the warning originates from application code or the third-party dependency stack.

---

## 27.6 `.venv` Active While Running Git Commands

### Question

Is it safe to commit/push while the prompt shows `(.venv)`?

### Answer

Yes.

The virtual environment affects commands such as:

```text
python
pip
pytest
ruff
uvicorn
```

It does not alter Git's behavior.

Valid:

```bash
git status
git add .
git commit
git push
```

while `.venv` is active.

### Required safety check

```bash
git check-ignore -v .venv
```

The `.venv/` directory must be ignored.

To exit the environment later:

```bash
deactivate
```

---

# 28. Pre-Commit Validation

Run all commands from repository root:

```bash
ruff format .
ruff check .
ruff format --check .
pytest -q
git diff --check
git status
```

Expected test result:

```text
5 passed
```

No output from `git diff --check` means no whitespace errors were found.

---

# 29. Stage Phase 01

```bash
git add \
  .github/workflows/01-ci.yml \
  .gitignore \
  .python-version \
  app \
  data \
  docs/phases/01-repository-fastapi-baseline.md \
  pyproject.toml \
  simulator \
  tests
```

Review:

```bash
git status
git diff --cached --check
git diff --cached --name-only
git diff --cached --stat
```

Must **not** include:

```text
.venv/
.env
*.egg-info/
__pycache__/
terraform.tfstate
terraform.tfvars
```

Inspect the actual staged diff:

```bash
git diff --cached
```

---

# 30. Commit Phase 01

```bash
git commit -m "feat: establish FastAPI edge inference baseline"
```

Verify:

```bash
git status
git log --oneline -5
```

---

# 31. Push the Feature Branch

```bash
git push -u origin feature/phase-01-fastapi-baseline
```

---

# 32. Create the Pull Request

Using GitHub CLI:

```bash
gh pr create \
  --base main \
  --head feature/phase-01-fastapi-baseline \
  --title "Phase 01: FastAPI edge inference baseline" \
  --body "Establishes the initial Industrial Edge AI application baseline with telemetry schema validation, FastAPI inference, simulated sensor replay, Prometheus metrics, automated tests, Ruff validation, and GitHub Actions CI."
```

Or in GitHub:

```text
Repository
  → Pull requests
  → New pull request
```

Select:

```text
base: main
compare: feature/phase-01-fastapi-baseline
```

---

# 33. Validate GitHub Actions

Navigate:

```text
GitHub
  → Repository
  → Actions
  → 01 - Python CI
  → latest workflow run
  → Validate Python
```

Required green steps:

```text
Checkout repository
Set up Python
Upgrade pip
Install project
Ruff lint
Ruff format check
Run tests
```

If any step fails: **do not merge**.

Fix locally, rerun local checks, commit, and push. GitHub automatically reruns the pull-request workflow.

---

# 34. Merge

Merge only when required checks pass.

For a self-contained phase branch, `Squash and merge` is a reasonable policy if it matches the repository's chosen history strategy.

---

# 35. Post-Merge Validation

Return to Mac:

```bash
git checkout main
git pull --ff-only
git status
```

Expected:

```text
On branch main
nothing to commit, working tree clean
```

Activate the environment if needed:

```bash
source .venv/bin/activate
```

Reinstall after merge if project dependencies changed:

```bash
pip install -e '.[dev]'
```

Run:

```bash
ruff check .
ruff format --check .
pytest -q
```

Start FastAPI if not already running:

```bash
uvicorn app.main:app --host 127.0.0.1 --port 8000
```

From another terminal:

```bash
curl http://127.0.0.1:8000/health
python simulator/replay.py --interval 0.2
curl -s http://127.0.0.1:8000/metrics | grep edgeai_
```

---

# 36. Validate CI on `main`

The workflow also contains:

```yaml
push:
  branches:
    - main
```

Therefore the merge should trigger CI again.

Final required state:

```text
Local feature tests   PASS
Pull Request CI       PASS
Merge                 COMPLETE
main CI               PASS
Local main tests      PASS
```

Only then mark Phase 01 complete.

---

# 37. Evidence to Capture

Recommended evidence for the project runbook/portfolio:

1. `pytest -q` output showing all tests passed.
2. `ruff check .` result.
3. `/health` response.
4. `/ready` response.
5. simulator output showing normal and critical predictions.
6. `/metrics` output containing `edgeai_*` metrics.
7. `git diff --cached --check` returning no output.
8. pull-request number/link.
9. PR GitHub Actions run with all checks green.
10. merged commit on `main`.
11. `main` GitHub Actions run with all checks green.
12. final local validation from updated `main`.

Never capture or commit secrets, tokens, `.env` files, Azure credentials, or future Terraform state.

---

# 38. Quick Troubleshooting Matrix

| Symptom | Root Cause | Validation | Fix |
|---|---|---|---|
| `Multiple top-level packages discovered` | `setuptools` package discovery ambiguous | Review repository top-level directories | Explicit `[tool.setuptools.packages.find]` |
| `*.egg-info/` untracked | Generated Python package metadata | `git status` | Add `*.egg-info/` to `.gitignore` and delete directory |
| `Connection refused` from simulator | API not listening | `curl /health`, `lsof :8000` | Start Uvicorn first |
| `Address already in use` | Port 8000 already owned | `lsof -iTCP:8000 -sTCP:LISTEN` | Reuse valid server or stop stale process |
| Pytest passes with warning | Dependency deprecation/compatibility warning | `pip show fastapi starlette httpx` | Investigate compatible dependency versions; do not suppress blindly |
| `.venv` active during Git | Not an error | `git check-ignore -v .venv` | Safe to continue; ensure `.venv/` is ignored |
| GitHub CI fails | Fresh runner found a reproducibility issue | Open failed workflow step | Reproduce locally, fix, commit, push, rerun CI |

---

# 39. What Phase 01 Proves

```text
Repository structure          PROVEN
Python package installation   PROVEN
Telemetry validation          PROVEN
FastAPI service               PROVEN
Predictor abstraction         PROVEN
Synthetic inference path      PROVEN
Sensor simulation             PROVEN
Prometheus metrics            PROVEN
Automated tests               PROVEN
Code-quality checks           PROVEN
Git feature workflow          PROVEN after merge
GitHub CI reproducibility     PROVEN after green CI
```

---

# 40. What Phase 01 Does Not Prove

The following remain intentionally out of scope:

```text
Azure connectivity
Terraform
Azure remote Terraform state
GitHub OIDC
IoT Hub
Event Hubs
ADLS Gen2
Databricks
Unity Catalog
MLflow
ONNX
Docker
ACR
AKS
IoT Edge
NVIDIA Jetson
GPU inference
production model accuracy
private networking
production SLOs
```

---

# 41. Phase 01 Closure Statement

Phase 01 can be marked **COMPLETE** only after:

```text
Local validation  → PASS
PR CI             → PASS
PR merge          → COMPLETE
main CI           → PASS
Post-merge local  → PASS
```

After that, development can begin on:

```text
Phase 02 — Terraform Bootstrap & Azure Remote State
```

using a new feature branch created from clean, updated `main`.

---

# Phase 01 — Command Validation & Troubleshooting Appendix

> [!NOTE]

> It does **not** repeat the implementation steps. It records command purpose, observed results, issues, fixes, and the correct action when the same condition occurs again.

---

## Status Legend

| Indicator | Meaning |
|---|---|
| 🟢 **PASS** | Command completed successfully |
| 🔵 **INFO** | Informational output; no action required |
| 🟡 **ACTION** | Follow-up action required |
| 🔴 **ERROR** | Command failed and must be corrected before continuing |
| ⚪ **EXPECTED** | Normal behavior for the command |

---

# 1. `Requirement already satisfied`

### Command Context

Observed during:

```bash
pip install -e '.[dev]'
```

Example output:

```text
Requirement already satisfied: packaging>=20 ...
Requirement already satisfied: pluggy<2,>=1.5 ...
Requirement already satisfied: click>=7.0 ...
```

### Status

🔵 **INFO — Not an error**

### Purpose of the Command

```bash
pip install -e '.[dev]'
```

installs the current project in **editable mode** together with development dependencies defined in `pyproject.toml`.

Editable mode means source changes under the repository are immediately visible to Python without rebuilding and reinstalling the project after every code edit.

### What `Requirement already satisfied` Means

Pip checked the active virtual environment and found a compatible version already installed.

```text
dependency requested
        ↓
pip checks .venv
        ↓
compatible version already exists
        ↓
no reinstall required
```

### What To Do

No corrective action is required.

Continue unless pip later reports:

```text
ERROR
Failed building wheel
ResolutionImpossible
No matching distribution found
```

---

# 2. Editable Project Rebuilt Successfully

Observed output:

```text
Building editable for industrial-edge-ai-platform (pyproject.toml) ... done
Successfully built industrial-edge-ai-platform
```

and:

```text
Successfully installed ...
industrial-edge-ai-platform-0.1.0
```

### Status

🟢 **PASS**

### Purpose

This validates that:

```text
pyproject.toml
      ↓
setuptools
      ↓
editable wheel
      ↓
project installed into .venv
```

### What This Proves

The earlier Python package-discovery problem is no longer blocking installation.

### What To Do If This Fails

If the error mentions:

```text
Multiple top-level packages discovered
```

verify that `pyproject.toml` explicitly limits package discovery to `app`:

```toml
[tool.setuptools.packages.find]
where = ["."]
include = ["app", "app.*"]
exclude = [
    "data",
    "data.*",
    "simulator",
    "simulator.*",
    "tests",
    "tests.*",
    "docs",
    "docs.*",
    "infra",
    "infra.*"
]
namespaces = false
```

Then clean generated metadata:

```bash
rm -rf build dist *.egg-info
```

and retry:

```bash
pip install -e '.[dev]'
```

---

# 3. `pip show httpx2`

### Command

```bash
pip show httpx2
```

### Purpose

Confirms:

- package name,
- installed version,
- installation location,
- dependency relationships.

Observed:

```text
Name: httpx2
Version: 2.12.0
Location: .../.venv/lib/python3.12/site-packages
```

### Status

🟢 **PASS**

### Why This Was Checked

An earlier Pytest execution produced a Starlette test-client deprecation warning involving the HTTP test client.

After installing the compatible dependency, the warning disappeared from the final recorded test runs.

### What To Do If Package Is Missing

If the command returns:

```text
WARNING: Package(s) not found
```

run:

```bash
pip install -e '.[dev]'
```

Then verify again:

```bash
pip show httpx2
```

> [!IMPORTANT]
> Do not depend permanently on a package that was installed manually but is absent from `pyproject.toml`.
> If Phase 01 requires the dependency, define it in the project's development dependencies so GitHub Actions can reproduce the environment.

---

# 4. `pytest -q`

### Command

```bash
pytest -q
```

### Purpose

Runs the automated Phase 01 test suite in quiet mode.

Observed final result:

```text
.....
5 passed in 0.19s
```

### Status

🟢 **PASS — 5/5**

### What This Validates

The test suite verifies:

- health endpoint,
- healthy inference path,
- critical inference path,
- invalid telemetry rejection,
- metrics endpoint.

### If Tests Fail

Do **not** commit.

Run:

```bash
pytest -vv
```

for more detailed output.

For one failing test:

```bash
pytest tests/test_api.py::<test_name> -vv
```

Use the failure category to troubleshoot:

| Failure Type | First Check |
|---|---|
| Import error | `pip install -e '.[dev]'` |
| HTTP 404 | API route registration |
| HTTP 422 unexpectedly | Pydantic schema / payload |
| Wrong prediction | `RuleBasedPredictor` logic |
| Metrics assertion | `/metrics` route and Prometheus counters |

---

# 5. `ruff check .`

### Command

```bash
ruff check .
```

Observed:

```text
All checks passed!
```

### Purpose

Runs Ruff's configured **lint rules**.

### Status

🟢 **PASS**

### Important Distinction

```bash
ruff check .
```

checks lint problems.

It does **not** perform the same work as:

```bash
ruff format .
```

### If Lint Errors Are Reported

Try safe automatic fixes:

```bash
ruff check . --fix
```

Then validate again:

```bash
ruff check .
```

> [!WARNING]
> `ruff check . --fix` does not guarantee formatting issues are fixed. Linting and formatting are separate quality gates.

---

# 6. `ruff format --check .`

### Command

```bash
ruff format --check .
```

### Purpose

Checks whether supported Python files and Python code blocks are already formatted according to Ruff.

Initial result:

```text
unformatted: File would be reformatted
```

The affected file was:

```text
docs/01-repository-fastapi-baseline.md
```

### Status at Time of Error

🟡 **ACTION REQUIRED**

### Why `ruff check . --fix` Did Not Fix It

Because:

```bash
ruff check . --fix
```

fixes lint findings.

The formatting command is:

```bash
ruff format .
```

### Correct Fix

Run:

```bash
ruff format docs/01-repository-fastapi-baseline.md
```

Observed:

```text
1 file reformatted
```

Then verify:

```bash
ruff format --check docs/01-repository-fastapi-baseline.md
```

Observed:

```text
1 file already formatted
```

Finally validate the repository:

```bash
ruff format --check .
```

Observed final result:

```text
16 files already formatted
```

### Final Status

🟢 **PASS**

### What To Do Next Time

Use:

```text
ruff check .
    → lint validation

ruff check . --fix
    → lint auto-fix

ruff format .
    → actual formatting

ruff format --check .
    → formatting validation only
```

---

# 7. `git diff --check`

### Command

```bash
git diff --check
```

### Purpose

Checks **unstaged working-tree changes** for whitespace problems such as:

- trailing whitespace,
- space-before-tab issues,
- malformed whitespace.

Observed:

```text
<no output>
```

### Status

🟢 **PASS**

### Important Meaning

No output is the expected successful result.

---

# 8. `git diff --cached --check`

### Command

```bash
git diff --cached --check
```

### Purpose

Checks the content currently in the **Git staging area**.

This is different from:

```bash
git diff --check
```

because Git has two separate versions during development:

```text
working tree
     ↓
git add
     ↓
staging area
     ↓
git commit
```

---

## Issue: `new blank line at EOF`

Observed:

```text
docs/01-repository-fastapi-baseline.md:1740: new blank line at EOF.
```

### Status

🔴 **ERROR — Staged content was not ready to commit**

### Root Cause

The Markdown file ended with an additional blank line beyond the normal final newline.

The file was corrected in the working tree, but initially the corrected version had **not yet been restaged**.

This explains why:

```bash
git diff --check
```

passed while:

```bash
git diff --cached --check
```

still failed.

### Key Git Concept

```text
working tree file
      ≠
staged file
```

until:

```bash
git add <file>
```

is run again.

### Correct Fix

Normalize the file ending:

```bash
python3 - <<'PY'
from pathlib import Path

p = Path("docs/01-repository-fastapi-baseline.md")
p.write_text(p.read_text().rstrip() + "\n")
PY
```

Restage it:

```bash
git add docs/01-repository-fastapi-baseline.md
```

Then rerun:

```bash
git diff --cached --check
```

Observed final result:

```text
<no output>
```

### Final Status

🟢 **PASS**

> [!IMPORTANT]
> After modifying any file that was already staged, run `git add <file>` again.
> Otherwise Git still holds the older staged snapshot.

---

# 9. Accidentally Running an Error Message as a Shell Command

The following text was entered directly at the shell:

```text
docs/01-repository-fastapi-baseline.md:1740: new blank line at EOF.
```

Bash responded:

```text
bash: docs/01-repository-fastapi-baseline.md:1740:: No such file or directory
```

### Status

🔴 **USER COMMAND ERROR — Not a project failure**

### Root Cause

The line:

```text
docs/01-repository-fastapi-baseline.md:1740: new blank line at EOF.
```

was diagnostic output from Git.

It is not a command.

Bash interpreted:

```text
docs/01-repository-fastapi-baseline.md:1740:
```

as a file/program path and tried to execute it.

### Correct Action

Read diagnostic messages, then execute only the remediation command.

For this issue, the remediation command was the Python EOF-normalization block followed by:

```bash
git add docs/01-repository-fastapi-baseline.md
git diff --cached --check
```

---

# 10. Interrupted Heredoc Command

Observed shell text included:

```text
pyth^C - <<'PY'
```

### Status

🔵 **INFO**

### Meaning

`^C` means `Ctrl+C` interrupted the command before completion.

### What To Do

Simply rerun the complete command cleanly.

Example:

```bash
python3 - <<'PY'
from pathlib import Path

p = Path("docs/01-repository-fastapi-baseline.md")
p.write_text(p.read_text().rstrip() + "\n")
PY
```

Then validate the result.

No repository repair is normally required simply because a command was interrupted before execution.

---

# 11. `git status`

### Command

```bash
git status
```

### Purpose

Shows:

- current branch,
- staged files,
- unstaged modifications,
- untracked files.

Observed branch:

```text
feature/phase-01-fastapi-baseline
```

### Status

🟢 **PASS**

### Important Issue Observed Earlier

`pyproject.toml` appeared both under:

```text
Changes to be committed
```

and:

```text
Changes not staged for commit
```

### Meaning

The file had been staged and then modified again.

### Correct Fix

```bash
git add pyproject.toml
```

### General Rule

If the same file appears staged and modified:

```bash
git add <file>
```

again after reviewing the latest content.

Then:

```bash
git status
git diff --cached --check
```

---

# 12. `git diff --cached --name-only`

### Command

```bash
git diff --cached --name-only
```

### Purpose

Shows exactly which paths will be included in the next commit.

This is a pre-commit safety check.

### Why It Matters

It helps detect accidental inclusion of:

```text
.env
.venv/
*.egg-info/
.DS_Store
terraform.tfstate
terraform.tfvars
```

### Current Observation

The staged list contains Phase 01 source, tests, CI, data, Python configuration, and documentation.

---

# 13. `.venv` Ignore Validation

### Command

```bash
git status --ignored | grep .venv
```

Observed:

```text
.venv/
```

Then:

```bash
git check-ignore -v .venv
```

Observed:

```text
.gitignore:11:.venv/    .venv
```

### Purpose

Confirms that the local Python virtual environment cannot accidentally be added to Git through normal staging.

### Status

🟢 **PASS**

### What This Proves

The ignore rule is:

```text
.gitignore line 11
.venv/
```

### If `.venv` Is Not Ignored

Add:

```gitignore
.venv/
```

to `.gitignore`.

If already tracked accidentally:

```bash
git rm -r --cached .venv
```

Then:

```bash
git status
```

---

# 14. `git add` Pathspec Error

Attempted:

```bash
git add docs/phases/01-repository-fastapi-baseline-runbook.md
```

Observed:

```text
fatal: pathspec 'docs/phases/01-repository-fastapi-baseline-runbook.md'
did not match any files
```

### Status

🔴 **ERROR — Incorrect path**

### Root Cause

That exact file did not exist at that exact repository path.

Git does not search for similar filenames automatically.

### Correct Troubleshooting

Run:

```bash
find docs -maxdepth 3 -type f | sort
```

Observed:

```text
docs/.DS_Store
docs/01-repository-fastapi-baseline.md
docs/phases/01-repository-fastapi-baseline.md
```

Then use the actual path.

Example:

```bash
git add docs/01-repository-fastapi-baseline.md
```

### General Rule

Before staging a file when unsure of its location:

```bash
find <directory> -type f | sort
```

or:

```bash
ls -l <expected-path>
```

---

# 15. Duplicate Phase 01 Documentation Paths

Observed:

```text
docs/01-repository-fastapi-baseline.md
docs/phases/01-repository-fastapi-baseline.md
```

### Status

🟡 **REVIEW BEFORE COMMIT**

### Why This Matters

Two documents with nearly identical names can create:

- maintenance confusion,
- conflicting instructions,
- uncertainty about the canonical runbook.

### Recommended Action

Compare:

```bash
diff -q \
  docs/01-repository-fastapi-baseline.md \
  docs/phases/01-repository-fastapi-baseline.md
```

If different:

```bash
diff -u \
  docs/phases/01-repository-fastapi-baseline.md \
  docs/01-repository-fastapi-baseline.md | less
```

Decide which file is authoritative.

Recommended structure:

```text
docs/
└── phases/
    ├── 01-repository-fastapi-baseline.md
    └── 01-command-validation-troubleshooting-appendix.md
```

> [!WARNING]
> Do not delete either document until the contents have been compared.

---

# 16. `.DS_Store` Under `docs/`

Observed:

```text
docs/.DS_Store
```

### Status

🟡 **LOCAL CLEANUP**

### Purpose of `.DS_Store`

It is macOS Finder metadata.

It has no project value.

### Validate Ignore Rule

```bash
git check-ignore -v docs/.DS_Store
```

### Remove Local Copy

```bash
rm -f docs/.DS_Store
```

### Validate

```bash
find docs -name ".DS_Store"
```

Expected:

```text
<no output>
```

---

# 17. Final Combined Local Quality Gate

The following commands were executed:

```bash
ruff check .
ruff format --check .
pytest -q
git diff --cached --check
```

Observed final result:

```text
All checks passed!
16 files already formatted
.....
5 passed in 0.19s
```

and:

```text
git diff --cached --check
```

returned no output.

### Final Status

| Check | Result |
|---|---|
| Ruff lint | 🟢 PASS |
| Ruff formatting | 🟢 PASS |
| Pytest | 🟢 PASS — 5/5 |
| Staged whitespace validation | 🟢 PASS |

---

# 18. Command Purpose Quick Reference

| Command | Purpose | Success Indicator |
|---|---|---|
| `pip install -e '.[dev]'` | Install project + development dependencies in editable mode | `Successfully installed` |
| `pip show httpx2` | Verify package/version/location | Package details shown |
| `pytest -q` | Run automated tests | `5 passed` |
| `ruff check .` | Lint repository | `All checks passed!` |
| `ruff check . --fix` | Auto-fix supported lint findings | No remaining lint findings |
| `ruff format .` | Apply Ruff formatting | `file(s) reformatted` |
| `ruff format --check .` | Validate formatting without changing files | `files already formatted` |
| `git status` | Show branch/staged/unstaged state | Expected files only |
| `git diff --check` | Check unstaged whitespace | No output |
| `git diff --cached --check` | Check staged whitespace | No output |
| `git diff --cached --name-only` | List files included in next commit | Expected Phase 01 paths |
| `git add <file>` | Update staging area with latest file | File appears staged |
| `git check-ignore -v .venv` | Confirm `.venv` ignore rule | `.gitignore` rule shown |
| `find docs -maxdepth 3 -type f \| sort` | Discover real documentation paths | Existing paths listed |

---

# 19. Pre-Commit Decision Rule

> [!IMPORTANT]
> Do not commit because one command passed. Commit only after the entire gate passes.

Required:

```text
🟢 pip install / editable build
🟢 dependency verification
🟢 ruff check
🟢 ruff format --check
🟢 pytest
🟢 git diff --check
🟢 git diff --cached --check
🟢 .venv ignored
🟢 no generated files staged
🟡 duplicate documentation reviewed
🟡 .DS_Store removed/ignored
```

---

# 20. Final Pre-Commit Commands

After resolving the duplicate documentation decision:

```bash
ruff check .
ruff format --check .
pytest -q
git diff --check
git diff --cached --check
git status
git diff --cached --name-only
git diff --cached --stat
```

Expected:

```text
Ruff             PASS
Formatting       PASS
Pytest           5 passed
Working diff     no whitespace errors
Staged diff      no whitespace errors
Git status       only intended Phase 01 changes
Staged files     only intended project paths
```

At that point Phase 01 is ready for:

```text
commit
  ↓
push
  ↓
pull request
  ↓
GitHub Actions
  ↓
merge
  ↓
post-merge validation
```
