from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


RepairStatus = Literal["warning", "pending", "in_progress", "completed"]


class RepairBase(BaseModel):
    car_id: int = Field(gt=0)
    repair_type: str = Field(min_length=1, max_length=120)
    mechanic: str | None = Field(default=None, max_length=120)
    status: RepairStatus = "pending"
    cost_estimate: float | None = Field(default=None, ge=0)
    final_cost: float | None = Field(default=None, ge=0)

    @field_validator("repair_type")
    @classmethod
    def strip_repair_type(cls, value: str) -> str:
        return value.strip()

    @field_validator("mechanic")
    @classmethod
    def strip_mechanic(cls, value: str | None) -> str | None:
        if value is None:
            return None
        stripped = value.strip()
        return stripped or None


class RepairCreate(RepairBase):
    service_bay_id: int | None = Field(default=None, gt=0)


class RepairUpdate(BaseModel):
    repair_type: str | None = Field(default=None, min_length=1, max_length=120)
    mechanic: str | None = Field(default=None, max_length=120)
    status: RepairStatus | None = None
    cost_estimate: float | None = Field(default=None, ge=0)
    final_cost: float | None = Field(default=None, ge=0)
    service_bay_id: int | None = Field(default=None, gt=0)

    @field_validator("repair_type")
    @classmethod
    def strip_repair_type(cls, value: str | None) -> str | None:
        if value is None:
            return None
        return value.strip()

    @field_validator("mechanic")
    @classmethod
    def strip_mechanic(cls, value: str | None) -> str | None:
        if value is None:
            return None
        stripped = value.strip()
        return stripped or None


class RepairStatusUpdate(BaseModel):
    status: RepairStatus


class RepairCompletion(BaseModel):
    final_cost: float | None = Field(default=None, ge=0)


class RepairBayAssignment(BaseModel):
    bay_id: int = Field(gt=0)


class RepairRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    car_id: int
    repair_type: str
    mechanic: str | None
    status: RepairStatus
    cost_estimate: float | None
    final_cost: float | None
    created_at: datetime
    updated_at: datetime
    completed_at: datetime | None
    service_bay_id: int | None
    car_license_plate: str | None = None
    service_bay_name: str | None = None


class RepairWarningRead(BaseModel):
    repair_id: int
    car_id: int
    license_plate: str
    repair_type: str
    created_at: datetime
