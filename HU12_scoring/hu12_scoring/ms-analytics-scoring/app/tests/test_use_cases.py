import pytest
from unittest.mock import MagicMock
from uuid import uuid4
from app.application.use_cases.calculate_score_use_case import CalculateScoreUseCase
from app.application.use_cases.get_score_use_case import GetScoreUseCase
from app.application.use_cases.rank_zones_use_case import RankZonesUseCase
from app.domain.entities.zone_score import ZoneScore
from app.domain.entities.score_execution import ScoreExecution

INDICATORS = [
    {
        "zone_code": "Z001",
        "zone_name": "Zona Centro",
        "population_indicator": 0.8,
        "income_indicator": 0.7,
        "education_indicator": 0.6,
        "competition_indicator": 0.5,
    },
    {
        "zone_code": "Z002",
        "zone_name": "Zona Norte",
        "population_indicator": 0.6,
        "income_indicator": 0.5,
        "education_indicator": 0.4,
        "competition_indicator": 0.3,
    },
]

def make_zone_score(code="Z001", name="Zona Centro", score=0.85, rank=1):
    return ZoneScore(
        score_execution_id="exec-001",
        zone_code=code,
        zone_name=name,
        score_value=score,
        rank_position=rank,
    )

def test_calculate_score_success():
    service = MagicMock()
    service.execute_scoring.return_value = {
        "execution_id": str(uuid4()),
        "status": "completed",
        "total_zones": 2,
        "scores": [],
    }
    uc = CalculateScoreUseCase(service)
    result = uc.execute(INDICATORS, "cfg-001", "run-001")
    assert result["success"] is True
    assert result["data"]["total_zones"] == 2

def test_calculate_score_empty_indicators():
    service = MagicMock()
    uc = CalculateScoreUseCase(service)
    result = uc.execute([], "cfg-001", "run-001")
    assert result["success"] is False
    assert "empty" in result["error"].lower()

def test_calculate_score_service_error():
    service = MagicMock()
    service.execute_scoring.side_effect = Exception("DB error")
    uc = CalculateScoreUseCase(service)
    result = uc.execute(INDICATORS, "cfg-001", "run-001")
    assert result["success"] is False

def test_get_score_by_execution():
    service = MagicMock()
    service.get_scores_by_execution.return_value = [make_zone_score()]
    uc = GetScoreUseCase(service)
    result = uc.execute_by_execution("exec-001")
    assert result["success"] is True
    assert len(result["data"]["zones"]) == 1

def test_get_all_executions():
    service = MagicMock()
    ex = ScoreExecution(transformation_run_id="run-001", configuration_id="cfg-001")
    service.get_all_executions.return_value = [ex]
    uc = GetScoreUseCase(service)
    result = uc.execute_all_executions()
    assert result["success"] is True
    assert len(result["data"]["executions"]) == 1

def test_rank_zones():
    service = MagicMock()
    service.get_ranking.return_value = [
        make_zone_score("Z001", "Zona Centro", 0.85, 1),
        make_zone_score("Z002", "Zona Norte", 0.65, 2),
    ]
    uc = RankZonesUseCase(service)
    result = uc.execute("exec-001")
    assert result["success"] is True
    assert result["data"][0]["score"] == 0.85
    assert result["data"][0]["zone"] == "Zona Centro"
