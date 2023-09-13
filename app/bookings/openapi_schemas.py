from app.bookings.schemas import BookingSchema
from app.exceptions import BookingNotFoundException
from app.hotels.rooms.openapi_schemas import room_not_found_response
from app.users.openapi_schemas import auth_error_responses
from app.utils import openapi_example_factory

openapi_booking_list = {
    "operation_id": "booking_list",
    "summary": "Список бронирований",
    "response_model": list[BookingSchema],
    "response_description": "Успешный ответ",
    "responses": auth_error_responses,
}

openapi_booking_create = {
    "operation_id": "booking_post",
    "summary": "Добавление бронирования",
    "response_model": BookingSchema,
    "response_description": "Успешный ответ",
    "responses": auth_error_responses | room_not_found_response
}


booking_not_found_response = openapi_example_factory(
    status_code=404,
    description="Ошибка: бронирование с указанным id не найдено",
    examples=[("Бронирование не найдено", BookingNotFoundException.detail)]
)

openapi_booking_delete = {
    "operation_id": "booking_delete",
    "summary": "Удаление бронирования",
    "status_code": 204,
    "response_description": "Бронирование успешно удалено",
    "responses": auth_error_responses | booking_not_found_response
}
