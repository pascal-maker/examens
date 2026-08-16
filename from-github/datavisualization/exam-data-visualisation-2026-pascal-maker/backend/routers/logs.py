from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from backend.database import get_db_session
from backend.schemas.audit_log import AuditLogRead
from backend.services import GarageService


router = APIRouter(prefix="/api/v1/logs", tags=["Logs"])


@router.get("", response_model=list[AuditLogRead])
def list_logs(
    entity_type: str | None = Query(default=None),
    action: str | None = Query(default=None),
    limit: int = Query(default=200, ge=1, le=1000),
    session: Session = Depends(get_db_session),
) -> list[AuditLogRead]:
    logs = GarageService(session).logs.list(entity_type=entity_type, action=action, limit=limit)
    return [
        AuditLogRead.model_validate(
            {
                "id": log.id,
                "timestamp": log.timestamp,
                "entity_type": log.entity_type,
                "entity_id": log.entity_id,
                "action": log.action,
                "old_value_json": log.old_value_json,
                "new_value_json": log.new_value_json,
                "message": f"{log.entity_type} #{log.entity_id} {log.action.replace('_', ' ')}",
            }
        )
        for log in logs
    ]
