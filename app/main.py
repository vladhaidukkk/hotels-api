from datetime import date
from typing import Annotated

from fastapi import FastAPI, Query
from pydantic import BaseModel

app = FastAPI()


@app.get("/hotels")
def get_hotels(
        location: str,
        date_from: date,
        date_to: date,
        stars: Annotated[int | None, Query(ge=1, le=5)] = None,
):
    return {
        "location": location,
        "date_from": date_from,
        "date_to": date_to,
        "stars": stars,
    }


class BookingIn(BaseModel):
    hotel_id: int
    room_id: int
    date_from: date
    date_to: date


@app.post("/bookings")
def create_booking(booking: BookingIn):
    return booking
