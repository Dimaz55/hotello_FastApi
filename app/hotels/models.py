from typing import List

from sqlalchemy import JSON, Column, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base


class Hotel(Base):
    __tablename__ = "hotels"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    location: Mapped[str] = mapped_column(nullable=False)
    services: Mapped[str] = mapped_column(JSON)
    rooms_quantity: Mapped[int] = mapped_column(nullable=False)
    image_id: Mapped[int] = mapped_column()
    rooms: Mapped[List["Room"]] = relationship(back_populates="hotel")

    def __str__(self):
        return self.name
