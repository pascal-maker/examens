from sqlalchemy.orm import Session

from app_config import get_settings
from backend.models import Car, Repair, ServiceBay
from backend.services.garage import GarageService
from backend.schemas.car import CarCreate
from backend.schemas.repair import RepairCreate
from backend.schemas.service_bay import ServiceBayCreate


def seed_demo_data(session: Session) -> None:
    settings = get_settings()
    service = GarageService(session)
    student_name = settings.student_name

    if not session.query(ServiceBay).count():
        for payload in [
            ServiceBayCreate(bay_name="Bay A", bay_type="General Service", available=True, notes=f"Primary bay for {student_name}"),
            ServiceBayCreate(bay_name="Bay B", bay_type="Diagnostics", available=True, notes="Electrical and scan tools"),
            ServiceBayCreate(bay_name="Bay C", bay_type="Body Work", available=True, notes="Panel and paint prep"),
        ]:
            service.create_service_bay(payload)

    if not session.query(Car).count():
        for payload in [
            CarCreate(
                license_plate="GM-2026-01",
                brand="Toyota",
                model="Corolla",
                owner_name=f"{student_name} Demo Fleet",
                kilometrage=158000,
                maintenance_threshold=150000,
            ),
            CarCreate(
                license_plate="GM-2026-02",
                brand="BMW",
                model="320d",
                owner_name=f"{student_name} Logistics",
                kilometrage=91000,
                maintenance_threshold=120000,
            ),
            CarCreate(
                license_plate="GM-2026-03",
                brand="Ford",
                model="Transit",
                owner_name=f"{student_name} Delivery",
                kilometrage=212000,
                maintenance_threshold=200000,
            ),
        ]:
            service.create_car(payload)

    if not session.query(Repair).filter(Repair.status != "warning").count():
        cars = session.query(Car).order_by(Car.id).all()
        bays = session.query(ServiceBay).order_by(ServiceBay.id).all()

        created_repairs = [
            service.create_repair(
                RepairCreate(
                    car_id=cars[0].id,
                    repair_type="Brake pad replacement",
                    mechanic=f"Lead Mechanic {student_name}",
                    status="pending",
                    cost_estimate=320.0,
                    service_bay_id=bays[0].id,
                )
            ),
            service.create_repair(
                RepairCreate(
                    car_id=cars[1].id,
                    repair_type="Battery diagnostics",
                    mechanic="Jordan Sparks",
                    status="in_progress",
                    cost_estimate=180.0,
                    service_bay_id=bays[1].id,
                )
            ),
            service.create_repair(
                RepairCreate(
                    car_id=cars[2].id,
                    repair_type="Oil leak inspection",
                    mechanic="Taylor Stone",
                    status="pending",
                    cost_estimate=240.0,
                )
            ),
        ]
        service.start_repair(created_repairs[1].id)
