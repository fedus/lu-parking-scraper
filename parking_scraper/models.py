from typing import Optional
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import composite
from datetime import datetime

import dataclasses


@dataclasses.dataclass
class UsageDetail:
    disabled: Optional[int]
    ev: Optional[int]
    general: Optional[int]

class Base(DeclarativeBase):
    pass

class ParkingUsage(Base):
    __tablename__ = "parking_usage"

    id: Mapped[int] = mapped_column(primary_key=True)
    scraped_at: Mapped[datetime]

    name: Mapped[str]
    city: Mapped[str]

    total: Mapped[Optional[int]]
    used: Mapped[Optional[int]]
    free: Mapped[Optional[int]]

    disabled: Mapped[Optional[int]]
    ev: Mapped[Optional[int]]
    general: Mapped[Optional[int]]

    detail: Mapped[UsageDetail] = composite("disabled", "ev", "general")

    def __repr__(self) -> str:
        return f"Parking(id={self.id!r}, name={self.name!r}, city={self.city!r}), \
            total={self.total!r}, used={self.used!r}, free={self.free!r}"

class BikeUsage(Base):
    __tablename__ = "bike_usage"

    id: Mapped[int] = mapped_column(primary_key=True)
    scraped_at: Mapped[datetime]

    station_number: Mapped[Optional[int]]
    city: Mapped[str]
    station_name: Mapped[str]
    status: Mapped[Optional[str]]
    connected: Mapped[Optional[bool]]
    bikes: Mapped[Optional[int]]
    stands: Mapped[Optional[int]]
    capacity: Mapped[Optional[int]]
