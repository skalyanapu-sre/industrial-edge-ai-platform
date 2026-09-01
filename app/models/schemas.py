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

    severity: Literal[
        "normal",
        "watch",
        "critical",
    ]

    predicted_failure_mode: str

    reasons: list[str]

    model_backend: str
    model_version: str
