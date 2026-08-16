from datetime import datetime

from sqlalchemy import DateTime, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.database import Base


class Car(Base):
    __tablename__ = "cars"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    license_plate: Mapped[str] = mapped_column(String(32), unique=True, index=True)
    brand: Mapped[str] = mapped_column(String(80))
    model: Mapped[str] = mapped_column(String(80))
    owner_name: Mapped[str] = mapped_column(String(120))
    kilometrage: Mapped[int] = mapped_column(Integer)
    maintenance_threshold: Mapped[int] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    repairs = relationship(
        "Repair",
        back_populates="car",
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    current_bays = relationship("ServiceBay", back_populates="current_car")
