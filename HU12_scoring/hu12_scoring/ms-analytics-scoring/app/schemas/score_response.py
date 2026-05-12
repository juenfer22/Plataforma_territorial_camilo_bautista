from typing import Any, Dict, List, Optional


class ScoreResponse:
    """
    Standard API response structure.
    Follows contract defined by professor.
    """

    @staticmethod
    def success(data: Any, trace_id: str = "") -> Dict[str, Any]:
        """Build success response."""
        return {
            "success": True,
            "data": data,
            "error": None,
            "trace_id": trace_id,
        }

    @staticmethod
    def error(message: str, trace_id: str = "") -> Dict[str, Any]:
        """Build error response."""
        return {
            "success": False,
            "data": None,
            "error": message,
            "trace_id": trace_id,
        }

    @staticmethod
    def ranking(scores: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Build ranking response following professor contract."""
        return {
            "success": True,
            "data": [
                {
                    "zone": s["zone_name"],
                    "score": s["score_value"],
                    "level": s["score_level"],
                }
                for s in scores
            ],
            "error": None,
            "trace_id": "",
        }
