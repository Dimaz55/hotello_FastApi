from datetime import date

from app.hotels.openapi_schemas import openapi_hotel_get
from app.hotels.rooms.repo import RoomRepo
from app.hotels.rooms.schemas import RoomSchema
from app.hotels.router import router


@router.get("/{hotel_id}/rooms", operation_id="room_list", **openapi_hotel_get)
async def get_rooms(hotel_id: int, date_from: date, date_to: date
) -> list[RoomSchema]:
    """
    Ищет и выдаёт список свободных номеров в отеле на указанные даты
    """
    return await RoomRepo.find_all(hotel_id, date_from, date_to)
