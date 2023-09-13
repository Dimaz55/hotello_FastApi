from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from starlette import status
from starlette.responses import Response

from app.bookings.models import Booking
from app.bookings.repo import BookingRepo
from app.bookings.schemas import BookingSchema
from app.bookings.openapi_schemas import (
    openapi_booking_list,
    openapi_booking_create,
    openapi_booking_delete
)
from app.exceptions import RoomIsBusyException
from app.hotels.rooms.repo import RoomRepo
from app.logger import logger
from app.tasks.tasks import send_booking_confirmation
from app.users.dependencies import get_current_user
from app.users.models import User


router = APIRouter(
    prefix="/bookings",
    tags=["Бронирования"]
)


@router.get(path="", **openapi_booking_list)
async def get_all_user_bookings(
    user: Annotated[User, Depends(get_current_user)]
) -> list[BookingSchema]:
    """
    Возвращает список всех бронирований текущего пользователя.
    
    - **room_id**: Идентификатор забронированного номера
    - **user_id**: Идентификатор текущего пользователя
    - **date_from**: Дата начала бронирования (заезда)
    - **date_to**: Дата окончания бронирования (выезда)
    - **price**: Стоимость номера за сутки
    - **total_cost**: Общая стоимость бронирования
    - **total_days**: Общее количество дней
    """
    return await BookingRepo.find_all(user_id=user.id)


@router.post("", **openapi_booking_create)
async def add_booking(
    room_id: int,
    date_from: Annotated[date, Query(description="ГГГГ-ММ-ДД")],
    date_to: Annotated[date, Query(description="ГГГГ-ММ-ДД")],
    user: Annotated[User, Depends(get_current_user)]
):
    """
    Создаёт бронирование текущего пользователя.

    - **room_id**: Идентификатор бронируемого номера
    - **date_from**: Дата начала бронирования (заезда)
    - **date_to**: Дата окончания бронирования (выезда)
    """
    
    await RoomRepo.is_room_exists(room_id)
    new_booking: Booking = await BookingRepo.add(user.id, room_id, date_from, date_to)
    if not new_booking:
        raise RoomIsBusyException

    bd = new_booking.__dict__.copy()
    bd.pop("_sa_instance_state")
    try:
        send_booking_confirmation.delay(bd, user.email)
    except Exception as e:
        logger.error("Celery error", extra={"exc": e.args})
    return new_booking


@router.delete("/{booking_id}", **openapi_booking_delete)
async def delete_user_booking(
    booking_id: int,
    user: Annotated[User, Depends(get_current_user)]
):
    """
    Удаление бронирования текущего пользователя.

    - **booking_id**: Идентификатор бронирования
    """
    await BookingRepo.delete_one(user_id=user.id, booking_id=booking_id)
    return Response(status_code=204)
