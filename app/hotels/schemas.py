from typing import Optional, Sequence

from pydantic import BaseModel


class HotelSchema(BaseModel):
    id: int
    name: str
    location: str
    services: Optional[Sequence]
    rooms_quantity: int
    image_id: int


class HotelListSchema(HotelSchema):
    rooms_left: int
