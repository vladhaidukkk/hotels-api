from datetime import date
from typing import Annotated

from fastapi import FastAPI, Query
from pydantic import BaseModel, Field

app = FastAPI()


class Hotel(BaseModel):
    name: str
    city: str
    address: str
    stars: int = Field(ge=1, le=5)


hotels = [
    Hotel(name="Seaside Escape", city="Oceanview", address="123 Coastal Rd", stars=4),
    Hotel(name="Mountain Retreat", city="Highpeak", address="456 Alpine St", stars=5),
    Hotel(name="Urban Hotel Central", city="Metrocity", address="789 Main Blvd", stars=3)
]


@app.get("/hotels")
def get_hotels(
        location: str,
        date_from: date,
        date_to: date,
        stars: Annotated[int | None, Query(ge=1, le=5)] = None,
) -> list[Hotel]:
    result = []
    for hotel in hotels:
        if stars and stars != hotel.stars:
            continue
        if location not in hotel.city and location not in hotel.address:
            continue
        result.append(hotel)
    return result


class BookingIn(BaseModel):
    hotel_id: int
    room_id: int
    date_from: date
    date_to: date


@app.post("/bookings")
def create_booking(booking: BookingIn):
    return booking
