from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AuditLogRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    timestamp: datetime
    entity_type: str
    entity_id: int
    action: str
    old_value_json: dict | None
    new_value_json: dict | None
    message: str | None = None
