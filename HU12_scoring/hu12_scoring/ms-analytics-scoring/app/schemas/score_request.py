from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class IndicatorInput:
    """Input schema for a single zone indicator."""
    zone_code: str
    zone_name: str
    population_indicator: float
    income_indicator: float
    education_indicator: float
    competition_indicator: float
    composite_indicator_json: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "zone_code": self.zone_code,
            "zone_name": self.zone_name,
            "population_indicator": self.population_indicator,
            "income_indicator": self.income_indicator,
            "education_indicator": self.education_indicator,
            "competition_indicator": self.competition_indicator,
            "composite_indicator_json": self.composite_indicator_json,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "IndicatorInput":
        return cls(
            zone_code=data["zone_code"],
            zone_name=data["zone_name"],
            population_indicator=float(data["population_indicator"]),
            income_indicator=float(data["income_indicator"]),
            education_indicator=float(data["education_indicator"]),
            competition_indicator=float(data["competition_indicator"]),
            composite_indicator_json=data.get("composite_indicator_json", {}),
        )


@dataclass
class ScoreRequest:
    """Input schema for scoring execution request."""
    indicators: List[IndicatorInput]
    configuration_id: str
    transformation_run_id: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ScoreRequest":
        return cls(
            indicators=[IndicatorInput.from_dict(i) for i in data["indicators"]],
            configuration_id=data["configuration_id"],
            transformation_run_id=data["transformation_run_id"],
        )
