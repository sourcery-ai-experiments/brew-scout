import typing as t
from datetime import datetime

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .common import Base

if t.TYPE_CHECKING:
    from .cities import CityModel


class CoffeeShopModel(Base):
    __tablename__ = "shops"

    id: Mapped[int] = mapped_column(primary_key=True)
    city_id: Mapped[int] = mapped_column(ForeignKey("cities.id"))
    name: Mapped[str]
    web_url: Mapped[str]
    latitude: Mapped[float]
    longitude: Mapped[float]
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=True
    )

    city: Mapped["CityModel"] = relationship(back_populates="shops")
