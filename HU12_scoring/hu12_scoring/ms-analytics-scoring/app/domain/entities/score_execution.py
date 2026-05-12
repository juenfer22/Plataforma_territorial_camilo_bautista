from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict
from uuid import UUID, uuid4

@dataclass
class ScoreExecution:
    transformation_run_id: str
    configuration_id: str
    formula_version: str = "1.0.0"
    status: str = "pending"
    executed_at: datetime = field(default_factory=datetime.utcnow)
    execution_id: UUID = field(default_factory=uuid4)

    STATUS_PENDING = "pending"
    STATUS_RUNNING = "running"
    STATUS_COMPLETED = "completed"
    STATUS_FAILED = "failed"

    def mark_running(self) -> None:
        self.status = self.STATUS_RUNNING

    def mark_completed(self) -> None:
        self.status = self.STATUS_COMPLETED

    def mark_failed(self) -> None:
        self.status = self.STATUS_FAILED

    def to_dict(self) -> Dict[str, Any]:
        return {
            "execution_id": str(self.execution_id),
            "transformation_run_id": self.transformation_run_id,
            "configuration_id": self.configuration_id,
            "formula_version": self.formula_version,
            "status": self.status,
            "executed_at": self.executed_at.isoformat(),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ScoreExecution":
        return cls(
            execution_id=UUID(data["execution_id"]),
            transformation_run_id=data["transformation_run_id"],
            configuration_id=data["configuration_id"],
            formula_version=data.get("formula_version", "1.0.0"),
            status=data.get("status", "pending"),
            executed_at=datetime.fromisoformat(data["executed_at"]),
        )
