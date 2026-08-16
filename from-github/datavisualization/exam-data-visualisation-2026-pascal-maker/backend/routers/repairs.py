from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from backend.database import get_db_session
from backend.schemas.repair import (
    RepairBayAssignment,
    RepairCompletion,
    RepairCreate,
    RepairRead,
    RepairUpdate,
    RepairWarningRead,
)
from backend.services import GarageService


router = APIRouter(prefix="/api/v1/repairs", tags=["Repairs"])


def _to_repair_read(repair):
    return RepairRead.model_validate(
        {
            **GarageService.serialize_repair(repair),
            "created_at": repair.created_at,
            "updated_at": repair.updated_at,
            "car_license_plate": repair.car.license_plate if repair.car else None,
            "service_bay_name": repair.service_bay.bay_name if repair.service_bay else None,
        }
    )


@router.get("", response_model=list[RepairRead])
def list_repairs(session: Session = Depends(get_db_session)) -> list[RepairRead]:
    service = GarageService(session)
    return [_to_repair_read(repair) for repair in service.repairs.list()]


@router.post("", response_model=RepairRead, status_code=status.HTTP_201_CREATED)
def create_repair(payload: RepairCreate, session: Session = Depends(get_db_session)) -> RepairRead:
    return _to_repair_read(GarageService(session).create_repair(payload))


@router.patch("/{repair_id}", response_model=RepairRead)
def update_repair(
    repair_id: int,
    payload: RepairUpdate,
    session: Session = Depends(get_db_session),
) -> RepairRead:
    return _to_repair_read(GarageService(session).update_repair(repair_id, payload))


@router.delete("/{repair_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_repair(repair_id: int, session: Session = Depends(get_db_session)) -> None:
    GarageService(session).delete_repair(repair_id)


@router.post("/{repair_id}/start", response_model=RepairRead)
def start_repair(repair_id: int, session: Session = Depends(get_db_session)) -> RepairRead:
    return _to_repair_read(GarageService(session).start_repair(repair_id))


@router.post("/{repair_id}/complete", response_model=RepairRead)
def complete_repair(
    repair_id: int,
    payload: RepairCompletion,
    session: Session = Depends(get_db_session),
) -> RepairRead:
    return _to_repair_read(GarageService(session).complete_repair(repair_id, payload.final_cost))


@router.post("/{repair_id}/assign-bay", response_model=RepairRead)
def assign_repair_to_bay(
    repair_id: int,
    payload: RepairBayAssignment,
    session: Session = Depends(get_db_session),
) -> RepairRead:
    return _to_repair_read(GarageService(session).assign_repair_to_bay(repair_id, payload.bay_id))


@router.get("/warnings", response_model=list[RepairWarningRead])
def list_repair_warnings(session: Session = Depends(get_db_session)) -> list[RepairWarningRead]:
    service = GarageService(session)
    warnings: list[RepairWarningRead] = []
    for repair, car in service.repairs.list_warning_rows():
        warnings.append(
            RepairWarningRead(
                repair_id=repair.id,
                car_id=car.id,
                license_plate=car.license_plate,
                repair_type=repair.repair_type,
                created_at=repair.created_at,
            )
        )
    return warnings
