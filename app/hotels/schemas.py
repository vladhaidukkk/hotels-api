from pydantic import BaseModel, Field


class Hotel(BaseModel):
    id: int
    name: str
    location: str
    stars: int = Field(ge=1, le=5)
    services: list | None
