from typing import Dict
from app.domain.entities.indicator_result import IndicatorResult
from app.domain.interfaces.i_score_calculator import IScoreCalculator


class WeightedSumCalculator(IScoreCalculator):
    """
    Calculates score using weighted sum method.
    Follows SRP: only handles weighted sum calculation.
    Follows LSP: interchangeable with other calculators.
    """

    DEFAULT_WEIGHTS: Dict[str, float] = {
        "population_indicator": 0.25,
        "income_indicator": 0.25,
        "education_indicator": 0.25,
        "competition_indicator": 0.25,
    }

    def calculate(
        self,
        indicator: IndicatorResult,
        weights: Dict[str, float],
    ) -> float:
        """
        Calculate weighted sum score.

        Args:
            indicator (IndicatorResult): Zone indicators.
            weights (Dict[str, float]): Weights per indicator.

        Returns:
            float: Score value 0.0 to 1.0.
        """
        used_weights = weights if weights else self.DEFAULT_WEIGHTS

        score = (
            indicator.population_indicator * used_weights.get("population_indicator", 0.25)
            + indicator.income_indicator * used_weights.get("income_indicator", 0.25)
            + indicator.education_indicator * used_weights.get("education_indicator", 0.25)
            + indicator.competition_indicator * used_weights.get("competition_indicator", 0.25)
        )
        return round(max(0.0, min(1.0, score)), 4)
