# Phase 01 — Repository and FastAPI Baseline

## Objective

Build and validate the first independently runnable component
of the Industrial Edge AI Platform.

## Architecture

Sensor CSV
→ Simulator
→ FastAPI
→ Pydantic
→ Predictor
→ Prediction
→ Prometheus Metrics

## Components

- FastAPI
- Uvicorn
- Pydantic
- Prometheus Client
- Pytest
- Ruff
- GitHub Actions

## Validation

### Local API

```bash
curl http://127.0.0.1:8000/health