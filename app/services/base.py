from abc import ABC, abstractmethod

from app.models.schemas import Prediction, SensorReading


class Predictor(ABC):
    @abstractmethod
    def predict(self, reading: SensorReading) -> Prediction:
        raise NotImplementedError
