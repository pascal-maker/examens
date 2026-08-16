from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.database import get_db_session
from backend.services import GarageService


router = APIRouter(prefix="/api/v1/analytics", tags=["Analytics"])


@router.get("/repairs-per-day")
def repairs_per_day(session: Session = Depends(get_db_session)) -> list[dict]:
    rows = []
    for date, count in GarageService(session).repairs.repairs_per_day():
        rows.append({"date": date, "count": count})
    return rows


@router.get("/repair-status-costs")
def repair_status_costs(session: Session = Depends(get_db_session)) -> list[dict]:
    rows = []
    for label, value in GarageService(session).repairs.repair_status_costs():
        rows.append({"label": label, "value": value})
    return rows


@router.get("/repairs-per-mechanic")
def repairs_per_mechanic(session: Session = Depends(get_db_session)) -> list[dict]:
    rows = []
    for label, value in GarageService(session).repairs.repairs_per_mechanic():
        rows.append({"label": label, "value": value})
    return rows


@router.get("/warnings-per-car")
def warnings_per_car(session: Session = Depends(get_db_session)) -> list[dict]:
    rows = []
    for label, value in GarageService(session).repairs.warnings_per_car():
        rows.append({"label": label, "value": value})
    return rows


@router.get("/bay-usage")
def bay_usage(session: Session = Depends(get_db_session)) -> list[dict]:
    rows = []
    for label, value in GarageService(session).bays.bay_usage():
        rows.append({"label": label, "value": value})
    return rows
