from backend.routers.analytics import router as analytics_router
from backend.routers.cars import router as cars_router
from backend.routers.health import router as health_router
from backend.routers.logs import router as logs_router
from backend.routers.repairs import router as repairs_router
from backend.routers.service_bays import router as service_bays_router

__all__ = [
    "analytics_router",
    "cars_router",
    "health_router",
    "logs_router",
    "repairs_router",
    "service_bays_router",
]
