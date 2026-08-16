from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from backend.database import get_db_session
from backend.schemas.service_bay import (
    ServiceBayCarAssignment,
    ServiceBayCreate,
    ServiceBayRead,
)
from backend.services import GarageService


router = APIRouter(prefix="/api/v1/service-bays", tags=["Service Bays"])


def _to_bay_read(bay):
    active_repair_id = None
    for repair in bay.repairs:
        if repair.status != "completed" and repair.service_bay_id == bay.id:
            active_repair_id = repair.id
            break
    return ServiceBayRead.model_validate(
        {
            **GarageService.serialize_bay(bay),
            "current_license_plate": bay.current_car.license_plate if bay.current_car else None,
            "active_repair_id": active_repair_id,
            "created_at": bay.created_at,
            "updated_at": bay.updated_at,
        }
    )


@router.get("", response_model=list[ServiceBayRead])
def list_service_bays(session: Session = Depends(get_db_session)) -> list[ServiceBayRead]:
    service = GarageService(session)
    return [_to_bay_read(bay) for bay in service.bays.list()]


@router.post("", response_model=ServiceBayRead, status_code=status.HTTP_201_CREATED)
def create_service_bay(payload: ServiceBayCreate, session: Session = Depends(get_db_session)) -> ServiceBayRead:
    return _to_bay_read(GarageService(session).create_service_bay(payload))


@router.delete("/{bay_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_service_bay(bay_id: int, session: Session = Depends(get_db_session)) -> None:
    GarageService(session).delete_service_bay(bay_id)


@router.post("/{bay_id}/assign-car", response_model=ServiceBayRead)
def assign_car_to_bay(
    bay_id: int,
    payload: ServiceBayCarAssignment,
    session: Session = Depends(get_db_session),
) -> ServiceBayRead:
    service = GarageService(session)
    return _to_bay_read(service.assign_car_to_bay(payload.car_id, bay_id))


@router.post("/{bay_id}/release", response_model=ServiceBayRead)
def release_bay(bay_id: int, session: Session = Depends(get_db_session)) -> ServiceBayRead:
    return _to_bay_read(GarageService(session).release_service_bay(bay_id))
