from datetime import date

from fastapi import APIRouter
from fastapi_cache.decorator import cache

from app.exceptions import HotelNotFoundException
from app.hotels.openapi_schemas import openapi_hotel_get
from app.hotels.repo import HotelRepo
from app.hotels.schemas import HotelListSchema, HotelSchema

router = APIRouter(prefix="/hotels", tags=["Отели"])


@router.get("", summary="Список всех отелей")
@cache(expire=24*60*60)
async def get_all_hotels() -> list[HotelSchema]:
    """
    Возвращает список всех отелей
    
    - **name**: название отеля
    - **location**: адрес отеля
    - **services**: услуги предоставляемые отелем
    - **rooms_quantity**: количество номеров в отеле
    - **image_id**: идентификатор фотографии отеля
    """
    return await HotelRepo.find_all()


@router.get("/{location}", summary="Поиск свободных отелей")
@cache(expire=10)
async def get_hotels_by_location(
    location: str, date_from: date, date_to: date
) -> list[HotelListSchema]:
    """
    Ищет и выдаёт список отелей со свободными номерами на указанные даты,
    с поиском по строке адреса отеля (**location**), например **hotels/Алтай**
    
    - **name**: название отеля
    - **location**: адрес отеля
    - **services**: услуги предоставляемые отелем
    - **rooms_quantity**: количество номеров в отеле
    - **image_id**: идентификатор фотографии отеля
    - **rooms_left**: количество свободных номеров в отеле
    """
    return await HotelRepo.find_all(
        location=location, date_from=date_from, date_to=date_to
    )


@router.get("/id/{hotel_id}", operation_id="hotel_get", **openapi_hotel_get)
@cache(expire=60)
async def get_hotel_by_id(hotel_id: int) -> HotelSchema:
    """
    Возвращает отель по идентификатору

    - **name**: название отеля
    - **location**: адрес отеля
    - **services**: услуги предоставляемые отелем
    - **rooms_quantity**: количество номеров в отеле
    - **image_id**: идентификатор фотографии отеля
    """
    hotel = await HotelRepo.find_one_or_none(id=hotel_id)
    if not hotel:
        raise HotelNotFoundException
    return hotel
