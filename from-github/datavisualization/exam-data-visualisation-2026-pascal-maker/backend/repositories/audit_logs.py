from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.models import AuditLog


class AuditLogRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def add(self, log_entry: AuditLog) -> AuditLog:
        self.session.add(log_entry)
        self.session.flush()
        return log_entry

    def list(self, entity_type: str | None = None, action: str | None = None, limit: int = 200) -> list[AuditLog]:
        statement = select(AuditLog).order_by(AuditLog.timestamp.desc(), AuditLog.id.desc()).limit(limit)
        if entity_type:
            statement = statement.where(AuditLog.entity_type == entity_type)
        if action:
            statement = statement.where(AuditLog.action == action)
        return list(self.session.scalars(statement).all())
