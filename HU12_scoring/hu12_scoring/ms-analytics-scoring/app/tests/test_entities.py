import pytest
from app.domain.entities.zone_score import ZoneScore
from app.domain.entities.score_execution import ScoreExecution
from app.domain.entities.indicator_result import IndicatorResult

def make_indicator():
    return IndicatorResult(
        zone_code="Z001",
        zone_name="Zona Centro",
        transformation_run_id="run-001",
        population_indicator=0.8,
        income_indicator=0.7,
        education_indicator=0.6,
        competition_indicator=0.5,
    )

def make_zone_score():
    return ZoneScore(
        score_execution_id="exec-001",
        zone_code="Z001",
        zone_name="Zona Centro",
        score_value=0.85,
    )

def test_indicator_creation():
    ind = make_indicator()
    assert ind.zone_code == "Z001"
    assert ind.population_indicator == 0.8

def test_indicator_to_dict():
    ind = make_indicator()
    d = ind.to_dict()
    assert d["zone_code"] == "Z001"
    assert "indicator_id" in d

def test_indicator_from_dict():
    ind = make_indicator()
    restored = IndicatorResult.from_dict(ind.to_dict())
    assert restored.zone_code == ind.zone_code

def test_zone_score_level_high():
    zs = make_zone_score()
    assert zs.score_level == "alta oportunidad"

def test_zone_score_level_medium():
    zs = ZoneScore(score_execution_id="e1", zone_code="Z2", zone_name="Zona 2", score_value=0.65)
    assert zs.score_level == "media oportunidad"

def test_zone_score_level_low():
    zs = ZoneScore(score_execution_id="e1", zone_code="Z3", zone_name="Zona 3", score_value=0.45)
    assert zs.score_level == "baja oportunidad"

def test_zone_score_level_none():
    zs = ZoneScore(score_execution_id="e1", zone_code="Z4", zone_name="Zona 4", score_value=0.20)
    assert zs.score_level == "sin oportunidad"

def test_zone_score_to_dict():
    zs = make_zone_score()
    d = zs.to_dict()
    assert d["zone_code"] == "Z001"
    assert d["score_value"] == 0.85

def test_zone_score_from_dict():
    zs = make_zone_score()
    restored = ZoneScore.from_dict(zs.to_dict())
    assert restored.zone_code == zs.zone_code
    assert restored.score_value == zs.score_value

def test_score_execution_status():
    ex = ScoreExecution(transformation_run_id="run-001", configuration_id="cfg-001")
    assert ex.status == "pending"
    ex.mark_running()
    assert ex.status == "running"
    ex.mark_completed()
    assert ex.status == "completed"

def test_score_execution_to_dict():
    ex = ScoreExecution(transformation_run_id="run-001", configuration_id="cfg-001")
    d = ex.to_dict()
    assert d["transformation_run_id"] == "run-001"
    assert "execution_id" in d
