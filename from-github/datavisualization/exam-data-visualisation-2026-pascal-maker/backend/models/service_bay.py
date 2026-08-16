from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.database import Base


class ServiceBay(Base):
    __tablename__ = "service_bays"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    bay_name: Mapped[str] = mapped_column(String(80), unique=True, index=True)
    bay_type: Mapped[str] = mapped_column(String(80))
    available: Mapped[bool] = mapped_column(Boolean, default=True)
    notes: Mapped[str | None] = mapped_column(String(255), nullable=True)
    current_car_id: Mapped[int | None] = mapped_column(
        ForeignKey("cars.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    current_car = relationship("Car", back_populates="current_bays")
    repairs = relationship("Repair", back_populates="service_bay")
