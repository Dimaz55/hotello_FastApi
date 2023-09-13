import time
from datetime import date, datetime
from typing import Union

from sqlalchemy import and_, select
from sqlalchemy.sql.functions import func

from app.bookings.models import Booking
from app.db import async_session_maker
from app.exceptions import DatesValidationError, HotelNotFoundException
from app.hotels.models import Hotel
from app.hotels.rooms.models import Room
from app.logger import logger
from app.repository.base import BaseRepo


def validate_dates(date_from, date_to) -> Union[str, None]:
    if date_from >= date_to:
        return "date_to must be greater than date_from"
    if (date_to - date_from).days > 30:
        return "maximum allowed period is 30 days"


class HotelRepo(BaseRepo):
    model = Hotel

    @classmethod
    async def find_all(cls, **filters):
        print('start')
        start_time = time.time()
        async with async_session_maker() as session:
            if filters:
                date_from = filters.get("date_from")
                date_to = filters.get("date_to")
                location = filters.get("location")
                error = validate_dates(date_from, date_to)
                if error:
                    raise DatesValidationError(detail=error)
                busy_rooms = cls._get_busy_rooms_cte(date_from, date_to)
                hotels = cls._get_free_hotels_query(busy_rooms, location)
            else:
                hotels = select("*").select_from(Hotel)
            
            try:
                result = await session.execute(hotels)
                
                process_time = time.time() - start_time
                print(process_time)
                print('end')
                return result.mappings().all()
            except Exception as e:
                logger.error("Database connection error", extra={
                    "exception": e
                })

    @classmethod
    def _get_busy_rooms_cte(cls, date_from: date, date_to: date):
        return (
            select(Hotel.id, func.count(Booking.id).label("booking_count"))
            .join(Room, Hotel.id == Room.hotel_id)
            .join(Booking, Room.id == Booking.room_id)
            .where(and_(Booking.date_to >= date_from, Booking.date_from <= date_to))
            .group_by(Hotel.id)
            .cte("busy_rooms_cte")
        )

    @classmethod
    def _get_free_hotels_query(cls, busy_rooms, location: str):
        return (
            select(
                Hotel.id,
                Hotel.name,
                Hotel.location,
                Hotel.services,
                Hotel.rooms_quantity,
                Hotel.image_id,
                # func.coalesce(busy_rooms.c.booking_count, 0).label('busy'),
                (
                    func.sum(Room.quantity)
                    - func.coalesce(busy_rooms.c.booking_count, 0)
                ).label("rooms_left"),
            )
            .select_from(Room)
            .join(Hotel, Room.hotel_id == Hotel.id)
            .join(busy_rooms, Room.hotel_id == busy_rooms.c.id, isouter=True)
            .where(Hotel.location.icontains(location))
            .group_by(Hotel.id, busy_rooms.c.booking_count)
            .order_by(Hotel.id)
        )
    
    @classmethod
    async def is_exists(cls, hotel_id: int):
        hotel = await super().find_by_id(hotel_id)
        if not hotel:
            raise HotelNotFoundException
