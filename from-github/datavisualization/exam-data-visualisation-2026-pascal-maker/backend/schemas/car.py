from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


class CarBase(BaseModel):
    license_plate: str = Field(min_length=2, max_length=32)
    brand: str = Field(min_length=1, max_length=80)
    model: str = Field(min_length=1, max_length=80)
    owner_name: str = Field(min_length=1, max_length=120)
    kilometrage: int = Field(ge=0)
    maintenance_threshold: int = Field(ge=0)

    @field_validator("license_plate")
    @classmethod
    def normalize_license_plate(cls, value: str) -> str:
        return value.strip().upper()

    @field_validator("brand", "model", "owner_name")
    @classmethod
    def strip_strings(cls, value: str) -> str:
        return value.strip()


class CarCreate(CarBase):
    pass


class CarUpdate(BaseModel):
    license_plate: str | None = Field(default=None, min_length=2, max_length=32)
    brand: str | None = Field(default=None, min_length=1, max_length=80)
    model: str | None = Field(default=None, min_length=1, max_length=80)
    owner_name: str | None = Field(default=None, min_length=1, max_length=120)
    kilometrage: int | None = Field(default=None, ge=0)
    maintenance_threshold: int | None = Field(default=None, ge=0)

    @field_validator("license_plate")
    @classmethod
    def normalize_license_plate(cls, value: str | None) -> str | None:
        if value is None:
            return None
        return value.strip().upper()

    @field_validator("brand", "model", "owner_name")
    @classmethod
    def strip_strings(cls, value: str | None) -> str | None:
        if value is None:
            return None
        return value.strip()


class CarRead(CarBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime
    open_warning_count: int = 0
    assigned_bay_name: str | None = None


class CarBayAssignment(BaseModel):
    bay_id: int = Field(gt=0)


class MaintenanceWarningRead(BaseModel):
    car_id: int
    license_plate: str
    owner_name: str
    kilometrage: int
    maintenance_threshold: int
    warning_repair_id: int
    created_at: datetime
