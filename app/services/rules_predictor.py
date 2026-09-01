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
            reasons.append("Low return-to-supply temperature differential while fan speed is high.")

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
