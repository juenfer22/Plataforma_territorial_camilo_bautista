from typing import Any, Dict
from app.domain.interfaces.i_score_service import IScoreService


class GetScoreUseCase:
    """
    Use case: Retrieve scoring results.
    Follows SRP: only handles retrieval flow.
    """

    def __init__(self, service: IScoreService) -> None:
        self._service = service

    def execute_by_execution(self, execution_id: str) -> Dict[str, Any]:
        """Get scores for a specific execution."""
        try:
            scores = self._service.get_scores_by_execution(execution_id)
            return {
                "success": True,
                "data": {"zones": [s.to_dict() for s in scores]},
                "error": None,
                "trace_id": execution_id,
            }
        except Exception as e:
            return {"success": False, "data": None, "error": str(e), "trace_id": ""}

    def execute_all_executions(self) -> Dict[str, Any]:
        """Get all scoring executions."""
        try:
            executions = self._service.get_all_executions()
            return {
                "success": True,
                "data": {"executions": [e.to_dict() for e in executions]},
                "error": None,
                "trace_id": "",
            }
        except Exception as e:
            return {"success": False, "data": None, "error": str(e), "trace_id": ""}
