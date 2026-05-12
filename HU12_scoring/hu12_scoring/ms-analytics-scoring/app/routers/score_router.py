import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from typing import Any, Dict, List
from app.application.use_cases.calculate_score_use_case import CalculateScoreUseCase
from app.application.use_cases.get_score_use_case import GetScoreUseCase
from app.application.use_cases.rank_zones_use_case import RankZonesUseCase
from app.schemas.score_response import ScoreResponse


class ScoreRouter:
    """
    Router for score endpoints.
    Follows SRP: only handles routing and delegation.
    Follows DIP: depends on use case abstractions.
    """

    def __init__(
        self,
        calculate_uc: CalculateScoreUseCase,
        get_uc: GetScoreUseCase,
        rank_uc: RankZonesUseCase,
    ) -> None:
        self._calculate = calculate_uc
        self._get = get_uc
        self._rank = rank_uc

    def post_calculate(self, body: Dict[str, Any]) -> Dict[str, Any]:
        """POST /scores/calculate - Execute scoring."""
        indicators = body.get("indicators", [])
        configuration_id = body.get("configuration_id", "default")
        transformation_run_id = body.get("transformation_run_id", "default")
        return self._calculate.execute(indicators, configuration_id, transformation_run_id)

    def get_scores(self, execution_id: str) -> Dict[str, Any]:
        """GET /scores/{execution_id} - Get scores by execution."""
        return self._get.execute_by_execution(execution_id)

    def get_ranking(self, execution_id: str) -> Dict[str, Any]:
        """GET /scores/{execution_id}/ranking - Get ranked zones."""
        return self._rank.execute(execution_id)

    def get_executions(self) -> Dict[str, Any]:
        """GET /scores/executions - Get all executions."""
        return self._get.execute_all_executions()

    def get_health(self) -> Dict[str, Any]:
        """GET /health - Health check endpoint."""
        return ScoreResponse.success(
            data={"status": "healthy", "service": "ms-analytics-scoring"},
            trace_id="",
        )
