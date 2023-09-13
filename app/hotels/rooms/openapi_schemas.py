from app.exceptions import RoomNotFoundException
from app.utils import openapi_example_factory, DetailResponseSchema

room_not_found_response = openapi_example_factory(
    status_code=404,
    model=DetailResponseSchema,
    description="Ошибка: номер с указанным id не найден",
    examples=[("Номер не найден", RoomNotFoundException.detail)]
)
