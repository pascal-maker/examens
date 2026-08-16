from __future__ import annotations

from typing import Tuple

from sqlalchemy import Select, func, select
from sqlalchemy.orm import Session, joinedload

from backend.models import Car, Repair, ServiceBay


class CarRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get(self, car_id: int) -> Car | None:
        return self.session.get(Car, car_id)

    def get_by_license_plate(self, license_plate: str) -> Car | None:
        statement = select(Car).where(Car.license_plate == license_plate)
        return self.session.scalar(statement)

    def list(self) -> list[Car]:
        statement: Select[Tuple[Car]] = (
            select(Car)
            .options(
                joinedload(Car.current_bays),
                joinedload(Car.repairs),
            )
            .order_by(Car.id)
        )

        return list(
            self.session.scalars(statement)
            .unique()
            .all()
        )

    def add(self, car: Car) -> Car:
        self.session.add(car)
        self.session.flush()
        return car

    def delete(self, car: Car) -> None:
        self.session.delete(car)
        self.session.flush()

    def count_warning_repairs(self, car_id: int) -> int:
        statement = (
            select(func.count(Repair.id))
            .where(
                Repair.car_id == car_id,
                Repair.status == "warning",
            )
        )

        return int(self.session.scalar(statement) or 0)

    def get_open_warning(self, car_id: int) -> Repair | None:
        statement = (
            select(Repair)
            .where(
                Repair.car_id == car_id,
                Repair.status == "warning",
                Repair.repair_type == "Maintenance threshold exceeded",
            )
            .order_by(Repair.created_at.desc())
        )

        return self.session.scalar(statement)

    def list_warning_rows(self) -> list[Tuple[Car, Repair]]:
        statement = (
            select(Car, Repair)
            .join(Repair, Repair.car_id == Car.id)
            .where(Repair.status == "warning")
            .order_by(Repair.created_at.desc())
        )

        return list(
            self.session.execute(statement).all()
        )

    def release_car_from_bays(self, car_id: int) -> None:
        statement = select(ServiceBay).where(
            ServiceBay.current_car_id == car_id
        )

        for bay in self.session.scalars(statement).all():
            bay.current_car_id = None
            bay.available = True