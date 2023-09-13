from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    is_admin: Mapped[bool] = mapped_column(server_default="false", default=False)
    bookings: Mapped[list[int]] = relationship(
        "Booking", back_populates="user", cascade="all, delete-orphan"
    )

    def __str__(self):
        return f"User {self.email}"
