from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict
from uuid import UUID, uuid4

@dataclass
class IndicatorResult:
    zone_code: str
    zone_name: str
    transformation_run_id: str
    population_indicator: float
    income_indicator: float
    education_indicator: float
    competition_indicator: float
    composite_indicator_json: Dict[str, Any] = field(default_factory=dict)
    calculated_at: datetime = field(default_factory=datetime.utcnow)
    indicator_id: UUID = field(default_factory=uuid4)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "indicator_id": str(self.indicator_id),
            "zone_code": self.zone_code,
            "zone_name": self.zone_name,
            "transformation_run_id": self.transformation_run_id,
            "population_indicator": self.population_indicator,
            "income_indicator": self.income_indicator,
            "education_indicator": self.education_indicator,
            "competition_indicator": self.competition_indicator,
            "composite_indicator_json": self.composite_indicator_json,
            "calculated_at": self.calculated_at.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "IndicatorResult":
        return cls(
            indicator_id=UUID(data["indicator_id"]),
            zone_code=data["zone_code"],
            zone_name=data["zone_name"],
            transformation_run_id=data["transformation_run_id"],
            population_indicator=float(data["population_indicator"]),
            income_indicator=float(data["income_indicator"]),
            education_indicator=float(data["education_indicator"]),
            competition_indicator=float(data["competition_indicator"]),
            composite_indicator_json=data.get("composite_indicator_json", {}),
            calculated_at=datetime.fromisoformat(data["calculated_at"]),
        )
