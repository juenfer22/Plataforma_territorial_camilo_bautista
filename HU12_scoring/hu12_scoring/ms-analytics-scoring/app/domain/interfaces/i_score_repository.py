from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID
from app.domain.entities.zone_score import ZoneScore
from app.domain.entities.score_execution import ScoreExecution
from app.domain.entities.indicator_result import IndicatorResult

class IScoreRepository(ABC):
    @abstractmethod
    def save_execution(self, execution: ScoreExecution) -> ScoreExecution: pass
    @abstractmethod
    def save_zone_score(self, zone_score: ZoneScore) -> ZoneScore: pass
    @abstractmethod
    def save_indicator(self, indicator: IndicatorResult) -> IndicatorResult: pass
    @abstractmethod
    def find_execution_by_id(self, execution_id: UUID) -> Optional[ScoreExecution]: pass
    @abstractmethod
    def find_scores_by_execution(self, execution_id: UUID) -> List[ZoneScore]: pass
    @abstractmethod
    def find_all_scores(self) -> List[ZoneScore]: pass
    @abstractmethod
    def find_all_executions(self) -> List[ScoreExecution]: pass
