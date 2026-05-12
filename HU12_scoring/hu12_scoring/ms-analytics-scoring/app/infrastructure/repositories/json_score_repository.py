import json
import os
from typing import Any, Dict, List, Optional
from uuid import UUID
from app.domain.entities.indicator_result import IndicatorResult
from app.domain.entities.score_execution import ScoreExecution
from app.domain.entities.zone_score import ZoneScore
from app.domain.interfaces.i_score_repository import IScoreRepository


class JsonScoreRepository(IScoreRepository):
    """
    JSON file-based repository implementation.
    Follows DIP: implements IScoreRepository.
    Follows SRP: only handles JSON persistence.
    """

    def __init__(self, data_path: str) -> None:
        self._executions_path = os.path.join(data_path, "executions.json")
        self._scores_path = os.path.join(data_path, "scores.json")
        self._indicators_path = os.path.join(data_path, "indicators.json")
        self._ensure_files()

    def _ensure_files(self) -> None:
        os.makedirs(os.path.dirname(self._executions_path), exist_ok=True)
        for path in [self._executions_path, self._scores_path, self._indicators_path]:
            if not os.path.exists(path):
                self._write(path, [])

    def _read(self, path: str) -> List[Dict[str, Any]]:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _write(self, path: str, data: List[Dict[str, Any]]) -> None:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def save_execution(self, execution: ScoreExecution) -> ScoreExecution:
        data = self._read(self._executions_path)
        existing = [i for i, e in enumerate(data) if e["execution_id"] == str(execution.execution_id)]
        if existing:
            data[existing[0]] = execution.to_dict()
        else:
            data.append(execution.to_dict())
        self._write(self._executions_path, data)
        return execution

    def save_zone_score(self, zone_score: ZoneScore) -> ZoneScore:
        data = self._read(self._scores_path)
        existing = [i for i, s in enumerate(data) if s["zone_score_id"] == str(zone_score.zone_score_id)]
        if existing:
            data[existing[0]] = zone_score.to_dict()
        else:
            data.append(zone_score.to_dict())
        self._write(self._scores_path, data)
        return zone_score

    def save_indicator(self, indicator: IndicatorResult) -> IndicatorResult:
        data = self._read(self._indicators_path)
        data.append(indicator.to_dict())
        self._write(self._indicators_path, data)
        return indicator

    def find_execution_by_id(self, execution_id: UUID) -> Optional[ScoreExecution]:
        for item in self._read(self._executions_path):
            if item["execution_id"] == str(execution_id):
                return ScoreExecution.from_dict(item)
        return None

    def find_scores_by_execution(self, execution_id: UUID) -> List[ZoneScore]:
        return [
            ZoneScore.from_dict(item)
            for item in self._read(self._scores_path)
            if item["score_execution_id"] == str(execution_id)
        ]

    def find_all_scores(self) -> List[ZoneScore]:
        return [ZoneScore.from_dict(item) for item in self._read(self._scores_path)]

    def find_all_executions(self) -> List[ScoreExecution]:
        return [ScoreExecution.from_dict(item) for item in self._read(self._executions_path)]
