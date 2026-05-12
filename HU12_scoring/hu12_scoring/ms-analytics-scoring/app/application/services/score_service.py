from typing import Any, Dict, List
from app.domain.entities.indicator_result import IndicatorResult
from app.domain.entities.score_execution import ScoreExecution
from app.domain.entities.zone_score import ZoneScore
from app.domain.interfaces.i_score_calculator import IScoreCalculator
from app.domain.interfaces.i_score_repository import IScoreRepository
from app.domain.interfaces.i_score_service import IScoreService


class ScoreService(IScoreService):
    """
    Core scoring service implementation.
    Follows SRP, DIP, OCP principles.
    """

    def __init__(
        self,
        repository: IScoreRepository,
        calculator: IScoreCalculator,
    ) -> None:
        self._repository = repository
        self._calculator = calculator

    def execute_scoring(
        self,
        indicators: List[Dict[str, Any]],
        configuration_id: str,
        transformation_run_id: str,
    ) -> Dict[str, Any]:
        """
        Execute full scoring process for a list of zones.

        Args:
            indicators: List of zone indicator dictionaries.
            configuration_id: Configuration reference ID.
            transformation_run_id: Transformation reference ID.

        Returns:
            Dict with execution results and zone scores.
        """
        execution = ScoreExecution(
            transformation_run_id=transformation_run_id,
            configuration_id=configuration_id,
        )
        execution.mark_running()
        self._repository.save_execution(execution)

        weights = self._extract_weights(configuration_id)
        zone_scores = []

        for ind_data in indicators:
            indicator = IndicatorResult(
                zone_code=ind_data["zone_code"],
                zone_name=ind_data["zone_name"],
                transformation_run_id=transformation_run_id,
                population_indicator=float(ind_data.get("population_indicator", 0.0)),
                income_indicator=float(ind_data.get("income_indicator", 0.0)),
                education_indicator=float(ind_data.get("education_indicator", 0.0)),
                competition_indicator=float(ind_data.get("competition_indicator", 0.0)),
                composite_indicator_json=ind_data.get("composite_indicator_json", {}),
            )
            self._repository.save_indicator(indicator)

            score_value = self._calculator.calculate(indicator, weights)
            zone_score = ZoneScore(
                score_execution_id=str(execution.execution_id),
                zone_code=indicator.zone_code,
                zone_name=indicator.zone_name,
                score_value=score_value,
            )
            self._repository.save_zone_score(zone_score)
            zone_scores.append(zone_score)

        ranked = self._apply_ranking(zone_scores)
        for zs in ranked:
            self._repository.save_zone_score(zs)

        execution.mark_completed()
        self._repository.save_execution(execution)

        return {
            "execution_id": str(execution.execution_id),
            "status": execution.status,
            "total_zones": len(ranked),
            "scores": [zs.to_dict() for zs in ranked],
        }

    def get_scores_by_execution(self, execution_id: str) -> List[ZoneScore]:
        """Get all zone scores for an execution."""
        from uuid import UUID
        return self._repository.find_scores_by_execution(UUID(execution_id))

    def get_ranking(self, execution_id: str) -> List[ZoneScore]:
        """Get ranked zone scores for an execution."""
        from uuid import UUID
        scores = self._repository.find_scores_by_execution(UUID(execution_id))
        return sorted(scores, key=lambda x: x.score_value, reverse=True)

    def get_all_executions(self) -> List[ScoreExecution]:
        """Get all scoring executions."""
        return self._repository.find_all_executions()

    def _extract_weights(self, configuration_id: str) -> Dict[str, float]:
        """Extract weights from configuration."""
        return {
            "population_indicator": 0.25,
            "income_indicator": 0.25,
            "education_indicator": 0.25,
            "competition_indicator": 0.25,
        }

    def _apply_ranking(self, zone_scores: List[ZoneScore]) -> List[ZoneScore]:
        """Apply ranking positions to zone scores."""
        sorted_scores = sorted(
            zone_scores, key=lambda x: x.score_value, reverse=True
        )
        for position, zone_score in enumerate(sorted_scores, start=1):
            zone_score.rank_position = position
        return sorted_scores
