from pydantic import BaseModel


class DetailResponseSchema(BaseModel):
    detail: str


def openapi_example_factory(
    status_code: int,
    description: str,
    examples: list[tuple[str, str]],
    model: type[BaseModel] = DetailResponseSchema
) -> dict:
    """
    Создаёт примеры для http-ответов документации OpenApi
    
    :param status_code: Код ответа
    :param model: Модель (схема) ответа
    :param description: Описание
    :param examples: Список примеров из кортежей формата
                     ("Заголовок примера", "Значение примера")
    :return: Словарь с примерами в формате OpenApi
    """
    examples = [
        {"summary": example_title, "value": {"detail": example_value}}
        for example_title, example_value in examples
    ]
    result = {
        status_code: {
            "model": model,
            "description": description,
            "content": {
                "application/json": {
                    "examples": examples
                }
            }
        }
    }
    return result
