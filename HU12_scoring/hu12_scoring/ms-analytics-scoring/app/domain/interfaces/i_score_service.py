from abc import ABC, abstractmethod
from typing import Any, Dict, List
from app.domain.entities.zone_score import ZoneScore
from app.domain.entities.score_execution import ScoreExecution
from app.domain.entities.indicator_result import IndicatorResult

class IScoreService(ABC):
    @abstractmethod
    def execute_scoring(self, indicators: List[Dict[str, Any]], configuration_id: str, transformation_run_id: str) -> Dict[str, Any]: pass
    @abstractmethod
    def get_scores_by_execution(self, execution_id: str) -> List[ZoneScore]: pass
    @abstractmethod
    def get_ranking(self, execution_id: str) -> List[ZoneScore]: pass
    @abstractmethod
    def get_all_executions(self) -> List[ScoreExecution]: pass
