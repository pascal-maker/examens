from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.database import Base


class Repair(Base):
    __tablename__ = "repairs"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    car_id: Mapped[int] = mapped_column(
        ForeignKey("cars.id", ondelete="CASCADE"),
        index=True,
    )
    repair_type: Mapped[str] = mapped_column(String(120))
    mechanic: Mapped[str | None] = mapped_column(String(120), nullable=True)
    status: Mapped[str] = mapped_column(String(32), index=True)
    cost_estimate: Mapped[float | None] = mapped_column(Float, nullable=True)
    final_cost: Mapped[float | None] = mapped_column(Float, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    service_bay_id: Mapped[int | None] = mapped_column(
        ForeignKey("service_bays.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
    )

    car = relationship("Car", back_populates="repairs")
    service_bay = relationship("ServiceBay", back_populates="repairs")
