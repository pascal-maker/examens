from contextlib import asynccontextmanager

from fastapi import FastAPI

from app_config import get_settings
from backend.database import init_database
from backend.routers import (
    analytics_router,
    cars_router,
    health_router,
    logs_router,
    repairs_router,
    service_bays_router,
)


@asynccontextmanager
async def lifespan(_: FastAPI):
    init_database()
    yield


settings = get_settings()

app = FastAPI(
    title=f"Garage Management API - {settings.student_name}",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(health_router)
app.include_router(cars_router)
app.include_router(repairs_router)
app.include_router(service_bays_router)
app.include_router(analytics_router)
app.include_router(logs_router)
