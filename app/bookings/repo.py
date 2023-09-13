from datetime import date

from sqlalchemy import and_, delete, func, insert, select
from sqlalchemy.exc import SQLAlchemyError
from app.bookings.models import Booking
from app.db import async_session_maker
from app.exceptions import BookingNotFoundException
from app.hotels.rooms.models import Room
from app.hotels.rooms.repo import RoomRepo
from app.logger import logger
from app.repository.base import BaseRepo


class BookingRepo(BaseRepo):
    model = Booking

    @classmethod
    async def add(
        cls,
        user_id: int,
        room_id: int,
        date_from: date,
        date_to: date
    ):
        await RoomRepo.is_room_exists(room_id)
        booked_rooms = (
            select(Booking)
            .where(
                and_(
                    Booking.room_id == room_id,
                    Booking.date_from <= date_to,
                    Booking.date_to >= date_from,
                )
            )
            .cte("booked rooms")
        )

        get_rooms_left = (
            select((Room.quantity - func.count(booked_rooms.c.room_id)))
            .select_from(Room)
            .join(booked_rooms, booked_rooms.c.room_id == Room.id, isouter=True)
            .where(Room.id == room_id)
            .group_by(Room.quantity, booked_rooms.c.room_id)
        )

        async with async_session_maker() as session:
            rooms_left = await session.execute(get_rooms_left)

            rooms_left = rooms_left.scalar()

            if rooms_left > 0:
                get_price = select(Room.price).filter_by(id=room_id)
                price = await session.execute(get_price)
                price = price.scalar()

                add_booking = (
                    insert(Booking)
                    .values(
                        room_id=room_id,
                        user_id=user_id,
                        date_from=date_from,
                        date_to=date_to,
                        price=price,
                    )
                    .returning(Booking)
                )
                try:
                    new_booking = await session.execute(add_booking)
                    await session.commit()
                    return new_booking.scalar()
                except (SQLAlchemyError, Exception) as e:
                    if isinstance(e, SQLAlchemyError):
                        msg = "Database exception"
                    elif isinstance(e, Exception):
                        msg = "Unknown exception"
                    msg += "Cannot add booking"
                    extra = {
                        "room_id": room_id,
                        "user_id": user_id,
                        "date_from": date_from,
                        "date_to": date_to,
                    }
                    logger.error(msg, extra=extra, exc_info=True)
            else:
                return None

    @classmethod
    async def delete_one(cls, user_id: int, booking_id: int):
        async with async_session_maker() as session:
            stmt = select(Booking).where(
                Booking.user_id == user_id,
                Booking.id == booking_id
            )
            res = await session.execute(stmt)
            if not res.scalars().one_or_none():
                raise BookingNotFoundException
            stmt = delete(Booking).where(
                Booking.id == booking_id,
                Booking.user_id == user_id,
            )
            await session.execute(stmt)
            await session.commit()
