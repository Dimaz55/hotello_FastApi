from datetime import date

from sqlalchemy import and_, func, select
from sqlalchemy.sql.functions import count

from app.bookings.models import Booking
from app.db import async_session_maker
from app.exceptions import RoomNotFoundException
from app.hotels.models import Hotel
from app.hotels.rooms.models import Room
from app.repository.base import BaseRepo


class RoomRepo(BaseRepo):
    model = Room

    @classmethod
    async def find_all(cls, hotel_id: int, date_from: date, date_to: date):
        async with async_session_maker() as session:
            # with busy_rooms as(
            #   SELECT h.id, COALESCE(COUNT(r.id), 0) AS busy
            #   FROM hotels h
            #   JOIN rooms r ON r.hotel_id = h.id
            #   JOIN bookings b ON b.room_id = r.id
            #   WHERE b.date_to >= '2023-05-15' AND b.date_from <= '2023-06-30'
            #   GROUP BY h.id
            # )
            # SELECT
            #   r.id, r.hotel_id, r.name, r.description, r.services,
            #   r.price, r.quantity, r.image_id,
            #   (date '2023-06-30' - date '2023-05-15') * r.price AS total_cost,
            #   r.quantity - coalesce(br.busy, 0) AS rooms_left
            # FROM rooms r
            # LEFT JOIN busy_rooms br ON br.id = r.id
            # WHERE r.hotel_id = 2 AND r.quantity - COALESCE(br.busy, 0) > 0
            # GROUP BY r.id, r.name, br.busy

            busy_rooms = (
                select(Hotel.id, func.coalesce(count(Room.id), 0).label("busy"))
                .join(Room, Hotel.id == Room.hotel_id)
                .join(Booking, Room.id == Booking.room_id)
                .where(and_(Booking.date_to >= date_from, Booking.date_from <= date_to))
                .group_by(Hotel.id)
                .cte()
            )

            rooms = (
                select(
                    Room.__table__.columns,
                    (
                        (date_to - date_from).days * Room.price
                    ).label("total_cost"),
                    (
                        Room.quantity - func.coalesce(busy_rooms.c.busy, 0)
                    ).label("rooms_left"),
                )
                .join(busy_rooms, Room.id == busy_rooms.c.id, isouter=True)
                .where(
                    and_(
                        Room.hotel_id == hotel_id,
                        Room.quantity - func.coalesce(busy_rooms.c.busy, 0) > 0,
                    )
                )
                .group_by(Room.id, busy_rooms.c.busy)
            )

            result = await session.execute(rooms)
            return result.mappings().all()

    @classmethod
    async def is_room_exists(cls, room_id: int):
        room = await cls.find_by_id(room_id)
        if not room:
            raise RoomNotFoundException
        