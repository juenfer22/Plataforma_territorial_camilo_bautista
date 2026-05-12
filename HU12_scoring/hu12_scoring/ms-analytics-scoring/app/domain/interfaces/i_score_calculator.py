from abc import ABC, abstractmethod
from typing import Dict
from app.domain.entities.indicator_result import IndicatorResult

class IScoreCalculator(ABC):
    @abstractmethod
    def calculate(self, indicator: IndicatorResult, weights: Dict[str, float]) -> float: pass
