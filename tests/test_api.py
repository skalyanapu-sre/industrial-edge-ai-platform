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
    response = client.post(
        "/v1/predict",
        json=HEALTHY_PAYLOAD,
    )

    assert response.status_code == 200

    body = response.json()

    assert body["severity"] == "normal"
    assert body["risk_score"] == 0.0


def test_critical_prediction() -> None:
    response = client.post(
        "/v1/predict",
        json=CRITICAL_PAYLOAD,
    )

    assert response.status_code == 200

    body = response.json()

    assert body["severity"] == "critical"
    assert body["risk_score"] == 1.0


def test_invalid_humidity_is_rejected() -> None:
    payload = HEALTHY_PAYLOAD.copy()

    payload["humidity_pct"] = 150

    response = client.post(
        "/v1/predict",
        json=payload,
    )

    assert response.status_code == 422


def test_metrics_endpoint() -> None:
    response = client.get("/metrics")

    assert response.status_code == 200

    assert "edgeai_inference_requests_total" in response.text
