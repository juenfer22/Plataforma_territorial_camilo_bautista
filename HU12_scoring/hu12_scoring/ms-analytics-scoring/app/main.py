import sys
import os
from fastapi import FastAPI # type: ignore

# Permitir imports correctos
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.application.calculators.weighted_sum_calculator import WeightedSumCalculator
from app.application.services.score_service import ScoreService
from app.application.use_cases.calculate_score_use_case import CalculateScoreUseCase
from app.application.use_cases.get_score_use_case import GetScoreUseCase
from app.application.use_cases.rank_zones_use_case import RankZonesUseCase
from app.infrastructure.repositories.json_score_repository import JsonScoreRepository
from app.routers.score_router import ScoreRouter

# ✅ Crear app FastAPI
app = FastAPI(title="MS Analytics Scoring")

# 🔧 Construcción del router (tu lógica existente)
def build_router() -> ScoreRouter:
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    data_path = os.path.join(base_dir, "data")
    repository = JsonScoreRepository(data_path=data_path)
    calculator = WeightedSumCalculator()
    service = ScoreService(repository=repository, calculator=calculator)
    calculate_uc = CalculateScoreUseCase(service)
    get_uc = GetScoreUseCase(service)
    rank_uc = RankZonesUseCase(service)
    return ScoreRouter(calculate_uc, get_uc, rank_uc)

# Instancia global
router = build_router()

# =========================
# 🚀 ENDPOINTS
# =========================

@app.get("/")
def root():
    return {"message": "Scoring API funcionando"}

@app.get("/health")
def health():
    return router.get_health()

@app.post("/analytics/score")
def calculate_score(body: dict):
    return router.post_calculate(body)

@app.get("/analytics/score/{execution_id}")
def get_scores(execution_id: str):
    return router.get_scores(execution_id)

@app.get("/analytics/ranking/{execution_id}")
def get_ranking(execution_id: str):
    return router.get_ranking(execution_id)

@app.get("/analytics/executions")
def get_executions():
    return router.get_executions()

# =========================
# 🧪 DEMO LOCAL (NO BORRAR)
# =========================

def demo() -> None:
    sep = "=" * 60
    router = build_router()

    print(sep)
    print("  HU-12 - SCORING TERRITORIAL")
    print(sep)

    print("\n[HEALTH CHECK]")
    health = router.get_health()
    print(f"  Status : {health['data']['status']}")
    print(f"  Service: {health['data']['service']}")

    print("\n[1] CALCULAR SCORES")
    body = {
        "configuration_id": "cfg-001",
        "transformation_run_id": "run-001",
        "indicators": [
            {
                "zone_code": "Z001",
                "zone_name": "Zona Centro",
                "population_indicator": 0.85,
                "income_indicator": 0.78,
                "education_indicator": 0.72,
                "competition_indicator": 0.65,
            }
        ],
    }

    result = router.post_calculate(body)
    print(f"  Exito      : {result['success']}")
    print(f"  Execution  : {result['trace_id']}")

    execution_id = result["trace_id"]

    print("\n[2] OBTENER SCORES")
    result2 = router.get_scores(execution_id)
    for zone in result2["data"]["zones"]:
        print(f"  Zona: {zone['zone_name']} Score: {zone['score_value']} Nivel: {zone['score_level']}")

    print("\n" + sep)
    print("  DEMO COMPLETADA")
    print(sep)


if __name__ == "__main__":
    demo()