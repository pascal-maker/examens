from fastapi import APIRouter

from app_config import get_settings


router = APIRouter(tags=["Health"])


@router.get("/")
def root() -> dict[str, str]:
    settings = get_settings()
    return {
        "message": "Garage Management API is running.",
        "student_name": settings.student_name,
        "api_base_url": settings.garage_api_base_url,
    }


@router.get("/health")
def healthcheck() -> dict[str, str]:
    return {"status": "ok"}
