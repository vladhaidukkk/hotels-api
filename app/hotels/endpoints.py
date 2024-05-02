from contextlib import contextmanager
from datetime import date
from typing import Annotated, Generator, LiteralString, Self

from fastapi import APIRouter, Depends, Query
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, ConfigDict, Field, ValidationError, model_validator
from pydantic_core import PydanticCustomError
from sqlalchemy.sql import ColumnExpressionArgument, and_, select

from app.db.core import async_engine
from app.hotels.table import hotels_table

router = APIRouter(prefix="/hotels", tags=["Hotels"])


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


class Hotel(BaseModel):
    id: int
    name: str
    location: str
    stars: int = Field(ge=1, le=5)
    services: dict | None

    model_config = ConfigDict(from_attributes=True)


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


@router.get("", response_model=list[Hotel])
async def get_hotels(params: Annotated[HotelSearchParams, Depends()]):
    with raise_request_validation_error("query"):
        ValidatedHotelSearchParams.model_validate(params.model_dump())

    async with async_engine.begin() as conn:
        conditions: list[ColumnExpressionArgument[bool]] = [
            hotels_table.c.location.ilike(f"%{params.location}%")
        ]
        if params.stars:
            conditions.append(hotels_table.c.stars == params.stars)
        query = select(hotels_table).where(and_(*conditions))
        res = await conn.execute(query)
        hotels = res.all()

    return hotels
