from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ServiceBayCreate(BaseModel):
    bay_name: str = Field(min_length=1, max_length=80)
    bay_type: str = Field(min_length=1, max_length=80)
    available: bool = True
    notes: str | None = Field(default=None, max_length=255)

    @field_validator("bay_name", "bay_type", "notes")
    @classmethod
    def strip_values(cls, value: str | None) -> str | None:
        if value is None:
            return None
        stripped = value.strip()
        return stripped or None


class ServiceBayCarAssignment(BaseModel):
    car_id: int = Field(gt=0)


class ServiceBayRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    bay_name: str
    bay_type: str
    available: bool
    notes: str | None
    current_car_id: int | None
    current_license_plate: str | None = None
    active_repair_id: int | None = None
    created_at: datetime
    updated_at: datetime
