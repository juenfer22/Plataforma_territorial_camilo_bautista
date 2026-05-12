from typing import Any, Dict, List
from app.domain.interfaces.i_score_service import IScoreService


class CalculateScoreUseCase:
    """
    Use case: Execute territorial scoring.
    Follows SRP: only orchestrates scoring flow.
    """

    def __init__(self, service: IScoreService) -> None:
        self._service = service

    def execute(
        self,
        indicators: List[Dict[str, Any]],
        configuration_id: str,
        transformation_run_id: str,
    ) -> Dict[str, Any]:
        """Execute scoring for a list of zones."""
        try:
            if not indicators:
                return {
                    "success": False,
                    "data": None,
                    "error": "Indicators list cannot be empty.",
                    "trace_id": "",
                }
            result = self._service.execute_scoring(
                indicators, configuration_id, transformation_run_id
            )
            return {
                "success": True,
                "data": result,
                "error": None,
                "trace_id": result.get("execution_id", ""),
            }
        except Exception as e:
            return {
                "success": False,
                "data": None,
                "error": str(e),
                "trace_id": "",
            }
