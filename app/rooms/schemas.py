from pydantic import BaseModel


class RoomOut(BaseModel):
    id: int
    name: str
    description: str | None
    capacity: int
    services: list[str]
    price: int
    quantity: int
    hotel_id: int
