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


@router.post(
    "/v1/predict",
    response_model=Prediction,
)
def predict(
    reading: SensorReading,
) -> Prediction:
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
