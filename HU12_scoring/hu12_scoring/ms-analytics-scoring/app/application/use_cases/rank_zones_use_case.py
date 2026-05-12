from typing import Any, Dict
from app.domain.interfaces.i_score_service import IScoreService


class RankZonesUseCase:
    """
    Use case: Rank zones by score.
    Follows SRP: only handles ranking flow.
    """

    def __init__(self, service: IScoreService) -> None:
        self._service = service

    def execute(self, execution_id: str) -> Dict[str, Any]:
        """Get ranked zones for an execution."""
        try:
            scores = self._service.get_ranking(execution_id)
            ranking = [
                {
                    "zone": s.zone_name,
                    "score": s.score_value,
                    "level": s.score_level,
                    "rank": s.rank_position,
                }
                for s in scores
            ]
            return {
                "success": True,
                "data": ranking,
                "error": None,
                "trace_id": execution_id,
            }
        except Exception as e:
            return {"success": False, "data": None, "error": str(e), "trace_id": ""}
