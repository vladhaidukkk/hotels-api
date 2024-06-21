from pydantic import BaseModel, Field


class HotelBase(BaseModel):
    id: int
    name: str
    location: str
    stars: int = Field(ge=1, le=5)
    services: list | None


class HotelOut(HotelBase):
    pass


class HotelWithRoomDetailsOut(HotelBase):
    rooms_quantity: int
    rooms_left: int
