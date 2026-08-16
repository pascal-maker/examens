from __future__ import annotations

from sqlalchemy import func, select
from sqlalchemy.orm import Session, joinedload

from backend.models import Car, Repair, ServiceBay


class RepairRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get(self, repair_id: int) -> Repair | None:
        return self.session.get(Repair, repair_id)

    def list(self) -> list[Repair]:
        statement = (
            select(Repair)
            .options(joinedload(Repair.car), joinedload(Repair.service_bay))
            .order_by(Repair.created_at.desc(), Repair.id.desc())
        )
        return list(self.session.scalars(statement).unique().all())

    def add(self, repair: Repair) -> Repair:
        self.session.add(repair)
        self.session.flush()
        return repair

    def delete(self, repair: Repair) -> None:
        self.session.delete(repair)
        self.session.flush()

    def list_warning_rows(self) -> list[tuple[Repair, Car]]:
        statement = (
            select(Repair, Car)
            .join(Car, Car.id == Repair.car_id)
            .where(Repair.status == "warning")
            .order_by(Repair.created_at.desc())
        )
        return list(self.session.execute(statement).all())

    def active_repair_for_bay(self, bay_id: int) -> Repair | None:
        statement = (
            select(Repair)
            .where(Repair.service_bay_id == bay_id, Repair.status != "completed")
            .order_by(Repair.updated_at.desc())
        )
        return self.session.scalar(statement)

    def repairs_per_day(self) -> list[tuple[str, int]]:
        day_bucket = func.date_trunc("day", Repair.created_at)
        statement = (
            select(
                day_bucket,
                func.count(Repair.id),
            )
            .group_by(day_bucket)
            .order_by(day_bucket)
        )
        return [(row[0].date().isoformat(), int(row[1])) for row in self.session.execute(statement).all()]

    def repair_status_costs(self) -> list[tuple[str, float]]:
        statement = (
            select(
                Repair.status,
                func.coalesce(func.sum(Repair.final_cost), func.sum(Repair.cost_estimate), 0.0),
            )
            .group_by(Repair.status)
            .order_by(Repair.status)
        )
        return [(row[0], float(row[1] or 0.0)) for row in self.session.execute(statement).all()]

    def repairs_per_mechanic(self) -> list[tuple[str, int]]:
        statement = (
            select(
                func.coalesce(Repair.mechanic, "Unassigned"),
                func.count(Repair.id),
            )
            .group_by(func.coalesce(Repair.mechanic, "Unassigned"))
            .order_by(func.count(Repair.id).desc())
        )
        return [(row[0], int(row[1])) for row in self.session.execute(statement).all()]

    def warnings_per_car(self) -> list[tuple[str, int]]:
        statement = (
            select(Car.license_plate, func.count(Repair.id))
            .join(Car, Car.id == Repair.car_id)
            .where(Repair.status == "warning")
            .group_by(Car.license_plate)
            .order_by(func.count(Repair.id).desc(), Car.license_plate.asc())
        )
        return [(row[0], int(row[1])) for row in self.session.execute(statement).all()]
