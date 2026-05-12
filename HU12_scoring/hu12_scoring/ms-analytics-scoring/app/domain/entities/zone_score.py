from dataclasses import dataclass, field
from typing import Any, Dict
from uuid import UUID, uuid4

@dataclass
class ZoneScore:
    score_execution_id: str
    zone_code: str
    zone_name: str
    score_value: float
    rank_position: int = 0
    score_level: str = ""
    zone_score_id: UUID = field(default_factory=uuid4)

    LEVEL_HIGH = "alta oportunidad"
    LEVEL_MEDIUM = "media oportunidad"
    LEVEL_LOW = "baja oportunidad"
    LEVEL_NONE = "sin oportunidad"

    def __post_init__(self) -> None:
        if not self.score_level:
            self.score_level = self._calculate_level(self.score_value)

    @staticmethod
    def _calculate_level(score: float) -> str:
        if score >= 0.80:
            return ZoneScore.LEVEL_HIGH
        if score >= 0.60:
            return ZoneScore.LEVEL_MEDIUM
        if score >= 0.40:
            return ZoneScore.LEVEL_LOW
        return ZoneScore.LEVEL_NONE

    def to_dict(self) -> Dict[str, Any]:
        return {
            "zone_score_id": str(self.zone_score_id),
            "score_execution_id": self.score_execution_id,
            "zone_code": self.zone_code,
            "zone_name": self.zone_name,
            "score_value": round(self.score_value, 4),
            "rank_position": self.rank_position,
            "score_level": self.score_level,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ZoneScore":
        return cls(
            zone_score_id=UUID(data["zone_score_id"]),
            score_execution_id=data["score_execution_id"],
            zone_code=data["zone_code"],
            zone_name=data["zone_name"],
            score_value=float(data["score_value"]),
            rank_position=int(data.get("rank_position", 0)),
            score_level=data.get("score_level", ""),
        )
