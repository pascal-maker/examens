from __future__ import annotations

from sqlalchemy import case, func, select
from sqlalchemy.orm import Session, joinedload

from backend.models import Repair, ServiceBay


class ServiceBayRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get(self, bay_id: int) -> ServiceBay | None:
        return self.session.get(ServiceBay, bay_id)

    def get_by_name(self, bay_name: str) -> ServiceBay | None:
        statement = select(ServiceBay).where(ServiceBay.bay_name == bay_name)
        return self.session.scalar(statement)

    def list(self) -> list[ServiceBay]:
        statement = (
            select(ServiceBay)
            .options(joinedload(ServiceBay.current_car), joinedload(ServiceBay.repairs))
            .order_by(ServiceBay.id)
        )
        return list(self.session.scalars(statement).unique().all())

    def add(self, bay: ServiceBay) -> ServiceBay:
        self.session.add(bay)
        self.session.flush()
        return bay

    def delete(self, bay: ServiceBay) -> None:
        self.session.delete(bay)
        self.session.flush()

    def bay_usage(self) -> list[tuple[str, int]]:
        statement = (
            select(
                ServiceBay.bay_name,
                func.sum(case((ServiceBay.available.is_(False), 1), else_=0)),
            )
            .group_by(ServiceBay.bay_name)
            .order_by(ServiceBay.bay_name)
        )
        return [(row[0], int(row[1] or 0)) for row in self.session.execute(statement).all()]

    def clear_assignments(self, bay_id: int) -> None:
        statement = select(Repair).where(Repair.service_bay_id == bay_id, Repair.status != "completed")
        for repair in self.session.scalars(statement).all():
            repair.service_bay_id = None
