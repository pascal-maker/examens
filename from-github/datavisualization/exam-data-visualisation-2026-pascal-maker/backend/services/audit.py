from datetime import datetime, timezone

from backend.models import AuditLog
from backend.repositories import AuditLogRepository


def write_audit_log(
    audit_repo: AuditLogRepository,
    entity_type: str,
    entity_id: int,
    action: str,
    old_value_json: dict | None,
    new_value_json: dict | None,
) -> AuditLog:
    entry = AuditLog(
        timestamp=datetime.now(timezone.utc),
        entity_type=entity_type,
        entity_id=entity_id,
        action=action,
        old_value_json=old_value_json,
        new_value_json=new_value_json,
    )
    return audit_repo.add(entry)
