import pytest
from app.application.calculators.weighted_sum_calculator import WeightedSumCalculator
from app.application.calculators.normalizer import Normalizer
from app.domain.entities.indicator_result import IndicatorResult

def make_indicator(pop=0.8, inc=0.7, edu=0.6, comp=0.5):
    return IndicatorResult(
        zone_code="Z001",
        zone_name="Zona Centro",
        transformation_run_id="run-001",
        population_indicator=pop,
        income_indicator=inc,
        education_indicator=edu,
        competition_indicator=comp,
    )

@pytest.fixture
def calculator():
    return WeightedSumCalculator()

def test_weighted_sum_default_weights(calculator):
    ind = make_indicator()
    score = calculator.calculate(ind, {})
    expected = (0.8 + 0.7 + 0.6 + 0.5) / 4
    assert abs(score - expected) < 0.001

def test_weighted_sum_custom_weights(calculator):
    ind = make_indicator(pop=1.0, inc=0.0, edu=0.0, comp=0.0)
    weights = {
        "population_indicator": 1.0,
        "income_indicator": 0.0,
        "education_indicator": 0.0,
        "competition_indicator": 0.0,
    }
    score = calculator.calculate(ind, weights)
    assert score == 1.0

def test_weighted_sum_score_range(calculator):
    ind = make_indicator()
    score = calculator.calculate(ind, {})
    assert 0.0 <= score <= 1.0

def test_weighted_sum_zero_indicators(calculator):
    ind = make_indicator(0.0, 0.0, 0.0, 0.0)
    score = calculator.calculate(ind, {})
    assert score == 0.0

def test_normalizer_min_max():
    result = Normalizer.min_max(5.0, 0.0, 10.0)
    assert result == 0.5

def test_normalizer_min_max_boundary():
    assert Normalizer.min_max(0.0, 0.0, 10.0) == 0.0
    assert Normalizer.min_max(10.0, 0.0, 10.0) == 1.0

def test_normalizer_equal_min_max():
    result = Normalizer.min_max(5.0, 5.0, 5.0)
    assert result == 0.0

def test_normalizer_clamp():
    result = Normalizer.min_max(15.0, 0.0, 10.0)
    assert result == 1.0
