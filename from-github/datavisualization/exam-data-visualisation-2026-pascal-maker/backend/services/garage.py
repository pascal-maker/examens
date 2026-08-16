from datetime import datetime, timezone

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from backend.models import Car, Repair, ServiceBay
from backend.repositories import (
    AuditLogRepository,
    CarRepository,
    RepairRepository,
    ServiceBayRepository,
)
from backend.schemas.car import CarCreate, CarUpdate
from backend.schemas.repair import RepairCreate, RepairUpdate
from backend.schemas.service_bay import ServiceBayCreate
from backend.services.audit import write_audit_log


class GarageService:
    def __init__(self, session: Session):
        self.session = session
        self.cars = CarRepository(session)
        self.repairs = RepairRepository(session)
        self.bays = ServiceBayRepository(session)
        self.logs = AuditLogRepository(session)

    def create_car(self, payload: CarCreate) -> Car:
        if self.cars.get_by_license_plate(payload.license_plate):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Car with license plate {payload.license_plate} already exists.",
            )

        car = Car(**payload.model_dump())
        self.cars.add(car)
        self._ensure_warning_for_car(car)
        self.session.commit()
        self.session.refresh(car)
        write_audit_log(
            self.logs,
            "car",
            car.id,
            "created",
            None,
            self.serialize_car(car),
        )
        self.session.commit()
        self.session.refresh(car)
        return car

    def update_car(self, car_id: int, payload: CarUpdate) -> Car:
        car = self._require_car(car_id)
        old_value = self.serialize_car(car)
        updates = payload.model_dump(exclude_unset=True)

        if "license_plate" in updates:
            existing = self.cars.get_by_license_plate(updates["license_plate"])
            if existing and existing.id != car.id:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail=f"Car with license plate {updates['license_plate']} already exists.",
                )

        for field_name, value in updates.items():
            setattr(car, field_name, value)

        self._ensure_warning_for_car(car)
        self.session.commit()
        self.session.refresh(car)
        write_audit_log(
            self.logs,
            "car",
            car.id,
            "updated",
            old_value,
            self.serialize_car(car),
        )
        self.session.commit()
        self.session.refresh(car)
        return car

    def delete_car(self, car_id: int) -> None:
        car = self._require_car(car_id)
        old_value = self.serialize_car(car)
        self.cars.release_car_from_bays(car_id)
        self.cars.delete(car)
        self.session.commit()
        write_audit_log(self.logs, "car", car_id, "deleted", old_value, None)
        self.session.commit()

    def create_repair(self, payload: RepairCreate) -> Repair:
        car = self._require_car(payload.car_id)
        repair = Repair(
            car_id=car.id,
            repair_type=payload.repair_type,
            mechanic=payload.mechanic,
            status=payload.status,
            cost_estimate=payload.cost_estimate,
            final_cost=payload.final_cost,
        )
        self.repairs.add(repair)

        if payload.service_bay_id:
            self._assign_repair_to_bay_entity(repair, payload.service_bay_id)

        self.session.commit()
        self.session.refresh(repair)
        write_audit_log(
            self.logs,
            "repair",
            repair.id,
            "created",
            None,
            self.serialize_repair(repair),
        )
        self.session.commit()
        self.session.refresh(repair)
        return repair

    def update_repair(self, repair_id: int, payload: RepairUpdate) -> Repair:
        repair = self._require_repair(repair_id)
        old_value = self.serialize_repair(repair)
        updates = payload.model_dump(exclude_unset=True)

        requested_bay_id = updates.pop("service_bay_id", None) if "service_bay_id" in updates else None

        for field_name, value in updates.items():
            setattr(repair, field_name, value)

        if repair.status == "completed" and repair.completed_at is None:
            repair.completed_at = datetime.now(timezone.utc)
            if repair.service_bay_id:
                self.session.flush()
                self._release_bay(repair.service_bay_id)
        elif repair.status != "completed":
            repair.completed_at = None

        if "service_bay_id" in payload.model_fields_set:
            if requested_bay_id is None and repair.service_bay_id:
                self._release_bay(repair.service_bay_id)
                repair.service_bay_id = None
            elif requested_bay_id is not None:
                self._assign_repair_to_bay_entity(repair, requested_bay_id)

        self.session.commit()
        self.session.refresh(repair)
        write_audit_log(
            self.logs,
            "repair",
            repair.id,
            "updated",
            old_value,
            self.serialize_repair(repair),
        )
        self.session.commit()
        self.session.refresh(repair)
        return repair

    def delete_repair(self, repair_id: int) -> None:
        repair = self._require_repair(repair_id)
        old_value = self.serialize_repair(repair)
        if repair.service_bay_id:
            self._release_bay(repair.service_bay_id)
        self.repairs.delete(repair)
        self.session.commit()
        write_audit_log(self.logs, "repair", repair_id, "deleted", old_value, None)
        self.session.commit()

    def start_repair(self, repair_id: int) -> Repair:
        repair = self._require_repair(repair_id)
        if repair.status == "completed":
            raise HTTPException(status_code=400, detail="Completed repairs cannot be restarted.")
        if repair.service_bay_id is None:
            raise HTTPException(status_code=400, detail="Assign a service bay before starting the repair.")

        old_value = self.serialize_repair(repair)
        repair.status = "in_progress"
        self.session.commit()
        self.session.refresh(repair)
        write_audit_log(
            self.logs,
            "repair",
            repair.id,
            "started",
            old_value,
            self.serialize_repair(repair),
        )
        self.session.commit()
        self.session.refresh(repair)
        return repair

    def complete_repair(self, repair_id: int, final_cost: float | None = None) -> Repair:
        repair = self._require_repair(repair_id)
        old_value = self.serialize_repair(repair)
        repair.status = "completed"
        repair.completed_at = datetime.now(timezone.utc)
        if final_cost is not None:
            repair.final_cost = final_cost
        if repair.service_bay_id:
            self.session.flush()
            self._release_bay(repair.service_bay_id)

        self.session.commit()
        self.session.refresh(repair)
        write_audit_log(
            self.logs,
            "repair",
            repair.id,
            "completed",
            old_value,
            self.serialize_repair(repair),
        )
        self.session.commit()
        self.session.refresh(repair)
        return repair

    def assign_repair_to_bay(self, repair_id: int, bay_id: int) -> Repair:
        repair = self._require_repair(repair_id)
        old_value = self.serialize_repair(repair)
        self._assign_repair_to_bay_entity(repair, bay_id)
        self.session.commit()
        self.session.refresh(repair)
        write_audit_log(
            self.logs,
            "repair",
            repair.id,
            "bay_assigned",
            old_value,
            self.serialize_repair(repair),
        )
        self.session.commit()
        self.session.refresh(repair)
        return repair

    def create_service_bay(self, payload: ServiceBayCreate) -> ServiceBay:
        if self.bays.get_by_name(payload.bay_name):
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Service bay named {payload.bay_name} already exists.",
            )

        bay = ServiceBay(**payload.model_dump())
        self.bays.add(bay)
        self.session.commit()
        self.session.refresh(bay)
        write_audit_log(self.logs, "service_bay", bay.id, "created", None, self.serialize_bay(bay))
        self.session.commit()
        self.session.refresh(bay)
        return bay

    def delete_service_bay(self, bay_id: int) -> None:
        bay = self._require_bay(bay_id)
        old_value = self.serialize_bay(bay)
        if not bay.available or bay.current_car_id is not None:
            raise HTTPException(
                status_code=400,
                detail="Release the service bay before deleting it.",
            )
        self.bays.delete(bay)
        self.session.commit()
        write_audit_log(self.logs, "service_bay", bay_id, "deleted", old_value, None)
        self.session.commit()

    def assign_car_to_bay(self, car_id: int, bay_id: int) -> ServiceBay:
        car = self._require_car(car_id)
        bay = self._require_bay(bay_id)
        if not bay.available and bay.current_car_id != car.id:
            raise HTTPException(status_code=400, detail=f"Service bay {bay.bay_name} is already occupied.")

        old_value = self.serialize_bay(bay)
        bay.current_car_id = car.id
        bay.available = False
        self.session.commit()
        self.session.refresh(bay)
        write_audit_log(
            self.logs,
            "service_bay",
            bay.id,
            "car_assigned",
            old_value,
            self.serialize_bay(bay),
        )
        self.session.commit()
        self.session.refresh(bay)
        return bay

    def release_service_bay(self, bay_id: int) -> ServiceBay:
        bay = self._require_bay(bay_id)
        old_value = self.serialize_bay(bay)
        self._release_bay(bay_id)
        self.session.commit()
        self.session.refresh(bay)
        write_audit_log(
            self.logs,
            "service_bay",
            bay.id,
            "released",
            old_value,
            self.serialize_bay(bay),
        )
        self.session.commit()
        self.session.refresh(bay)
        return bay

    def _ensure_warning_for_car(self, car):
        if car.kilometrage <= car.maintenance_threshold:
            return
        existing_warning = self.cars.get_open_warning(car.id)
        if existing_warning:
            return

        warning = Repair(
            car_id=car.id,
            repair_type="Maintenance threshold exceeded",
            mechanic="System",
            status="warning",
            cost_estimate=0.0,
            final_cost=None,
        )
        self.repairs.add(warning)
        self.session.flush()
        write_audit_log(
            self.logs,
            "repair",
            warning.id,
            "warning_created",
            None,
            self.serialize_repair(warning),
        )

    def _assign_repair_to_bay_entity(self, repair, bay_id):
        bay = self._require_bay(bay_id)
        if repair.status == "completed":
            raise HTTPException(status_code=400, detail="Completed repairs cannot be assigned to a service bay.")

        occupying_repair = self.repairs.active_repair_for_bay(bay_id)
        if occupying_repair and occupying_repair.id != repair.id:
            raise HTTPException(
                status_code=400,
                detail=f"Service bay {bay.bay_name} is already assigned to repair #{occupying_repair.id}.",
            )

        if repair.service_bay_id and repair.service_bay_id != bay_id:
            self._release_bay(repair.service_bay_id)

        bay.current_car_id = repair.car_id
        bay.available = False
        repair.service_bay_id = bay.id

    def _release_bay(self, bay_id):
        bay = self._require_bay(bay_id)
        bay.current_car_id = None
        bay.available = True
        self.bays.clear_assignments(bay_id)

    def _require_car(self, car_id):
        car = self.cars.get(car_id)
        if not car:
            raise HTTPException(status_code=404, detail=f"Car {car_id} was not found.")
        return car

    def _require_repair(self, repair_id):
        repair = self.repairs.get(repair_id)
        if not repair:
            raise HTTPException(status_code=404, detail=f"Repair {repair_id} was not found.")
        return repair

    def _require_bay(self, bay_id):
        bay = self.bays.get(bay_id)
        if not bay:
            raise HTTPException(status_code=404, detail=f"Service bay {bay_id} was not found.")
        return bay

    @staticmethod
    def serialize_car(car: Car) -> dict:
        return {
            "id": car.id,
            "license_plate": car.license_plate,
            "brand": car.brand,
            "model": car.model,
            "owner_name": car.owner_name,
            "kilometrage": car.kilometrage,
            "maintenance_threshold": car.maintenance_threshold,
        }

    @staticmethod
    def serialize_repair(repair: Repair) -> dict:
        return {
            "id": repair.id,
            "car_id": repair.car_id,
            "repair_type": repair.repair_type,
            "mechanic": repair.mechanic,
            "status": repair.status,
            "cost_estimate": repair.cost_estimate,
            "final_cost": repair.final_cost,
            "service_bay_id": repair.service_bay_id,
            "completed_at": repair.completed_at.isoformat() if repair.completed_at else None,
        }

    @staticmethod
    def serialize_bay(bay: ServiceBay) -> dict:
        return {
            "id": bay.id,
            "bay_name": bay.bay_name,
            "bay_type": bay.bay_type,
            "available": bay.available,
            "notes": bay.notes,
            "current_car_id": bay.current_car_id,
        }
