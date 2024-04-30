from contextlib import contextmanager
from datetime import date, datetime
from typing import Annotated, Generator, LiteralString, Self

from fastapi import Depends, FastAPI, Query, status
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, Field, ValidationError, model_validator
from pydantic_core import PydanticCustomError

app = FastAPI()


class Hotel(BaseModel):
    name: str
    city: str
    address: str
    stars: int = Field(ge=1, le=5)


hotels = [
    Hotel(name="Seaside Escape", city="Oceanview", address="123 Coastal Rd", stars=4),
    Hotel(name="Mountain Retreat", city="Highpeak", address="456 Alpine St", stars=5),
    Hotel(
        name="Urban Hotel Central", city="Metrocity", address="789 Main Blvd", stars=3
    ),
]


def create_custom_error(
    error_type: LiteralString, message: LiteralString
) -> PydanticCustomError:
    return PydanticCustomError(error_type, message, {"error": {}})


@contextmanager
def raise_request_validation_error(
    loc: str | None = None,
) -> Generator[None, None, None]:
    try:
        yield
    except ValidationError as err:
        errors = err.errors()
        if loc:
            for error in errors:
                error["loc"] = (loc, *error["loc"])
        raise RequestValidationError(errors)


class HotelSearchParams(BaseModel):
    location: str
    date_from: date | None = None
    date_to: date | None = None
    stars: Annotated[int | None, Query(ge=1, le=5)] = None


class ValidatedHotelSearchParams(HotelSearchParams):
    @model_validator(mode="after")
    def validate_date_range(self) -> Self:
        if self.date_from and self.date_to and self.date_from > self.date_to:
            raise create_custom_error(
                "date_range_invalid",
                "Start date can't be greater than end date",
            )
        return self


@app.get("/hotels")
def get_hotels(params: Annotated[HotelSearchParams, Depends()]) -> list[Hotel]:
    with raise_request_validation_error("query"):
        ValidatedHotelSearchParams.model_validate(params.model_dump())

    result = []
    for hotel in hotels:
        if params.stars and params.stars != hotel.stars:
            continue
        if params.location not in hotel.city and params.location not in hotel.address:
            continue
        result.append(hotel)
    return result


class BaseBooking(BaseModel):
    hotel_id: int
    room_id: int
    date_from: date
    date_to: date


class Booking(BaseBooking):
    created_at: datetime
    updated_at: datetime


class BookingIn(BaseBooking):
    pass


class BookingOut(Booking):
    pass


bookings: list[Booking] = []


@app.post("/bookings", status_code=status.HTTP_201_CREATED, response_model=BookingOut)
def create_booking(booking: BookingIn) -> Booking:
    now = datetime.now()
    new_booking = Booking(**booking.model_dump(), created_at=now, updated_at=now)
    bookings.append(new_booking)
    return new_booking
