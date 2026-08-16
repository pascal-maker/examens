from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from backend.database import get_db_session
from backend.schemas.car import (
    CarBayAssignment,
    CarCreate,
    CarRead,
    CarUpdate,
    MaintenanceWarningRead,
)
from backend.services import GarageService


router = APIRouter(prefix="/api/v1/cars", tags=["Cars"])


def _to_car_read(car):
    assigned_bay_name = car.current_bays[0].bay_name if car.current_bays else None
    open_warning_count = sum(1 for repair in car.repairs if repair.status == "warning")
    return CarRead.model_validate(
        {
            **GarageService.serialize_car(car),
            "created_at": car.created_at,
            "updated_at": car.updated_at,
            "open_warning_count": open_warning_count,
            "assigned_bay_name": assigned_bay_name,
        }
    )


@router.get("", response_model=list[CarRead])
def list_cars(session: Session = Depends(get_db_session)) -> list[CarRead]:
    service = GarageService(session)
    return [_to_car_read(car) for car in service.cars.list()]


@router.post("", response_model=CarRead, status_code=status.HTTP_201_CREATED)
def create_car(payload: CarCreate, session: Session = Depends(get_db_session)) -> CarRead:
    service = GarageService(session)
    return _to_car_read(service.create_car(payload))


@router.patch("/{car_id}", response_model=CarRead)
def update_car(car_id: int, payload: CarUpdate, session: Session = Depends(get_db_session)) -> CarRead:
    service = GarageService(session)
    return _to_car_read(service.update_car(car_id, payload))


@router.delete("/{car_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_car(car_id: int, session: Session = Depends(get_db_session)) -> None:
    GarageService(session).delete_car(car_id)


@router.get("/warnings", response_model=list[MaintenanceWarningRead])
def list_warnings(session: Session = Depends(get_db_session)) -> list[MaintenanceWarningRead]:
    service = GarageService(session)
    warnings: list[MaintenanceWarningRead] = []
    for car, repair in service.cars.list_warning_rows():
        warnings.append(
            MaintenanceWarningRead(
                car_id=car.id,
                license_plate=car.license_plate,
                owner_name=car.owner_name,
                kilometrage=car.kilometrage,
                maintenance_threshold=car.maintenance_threshold,
                warning_repair_id=repair.id,
                created_at=repair.created_at,
            )
        )
    return warnings


@router.post("/{car_id}/assign-bay", response_model=CarRead)
def assign_car_to_bay(
    car_id: int,
    payload: CarBayAssignment,
    session: Session = Depends(get_db_session),
) -> CarRead:
    service = GarageService(session)
    service.assign_car_to_bay(car_id, payload.bay_id)
    updated_car = service.cars.get(car_id)
    return _to_car_read(updated_car)
