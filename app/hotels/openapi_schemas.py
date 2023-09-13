from app.exceptions import HotelNotFoundException
from app.utils import openapi_example_factory, DetailResponseSchema

hotel_not_found_response = openapi_example_factory(
    status_code=404,
    model=DetailResponseSchema,
    description="Ошибка: отель с указанным id не найден",
    examples=[("Отель не найден", HotelNotFoundException.detail)]
)

openapi_hotel_get = {
    "summary": "Получение отеля по id",
    "responses": hotel_not_found_response
}
