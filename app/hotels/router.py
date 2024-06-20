from datetime import date
from typing import Annotated, Self

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel, model_validator
from sqlalchemy.sql import ColumnExpressionArgument

from app.hotels.model import HotelModel
from app.hotels.repo import HotelsRepo
from app.hotels.schemas import Hotel
from app.validation import create_custom_error, raise_request_validation_error

router = APIRouter(prefix="/hotels", tags=["Hotels"])


class HotelSearchParams(BaseModel):
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


@router.get("/{location}", response_model=list[Hotel])
async def get_hotels(location: str, params: Annotated[HotelSearchParams, Depends()]):
    with raise_request_validation_error("query"):
        ValidatedHotelSearchParams.model_validate(params.model_dump())

    conditions: list[ColumnExpressionArgument[bool]] = [
        HotelModel.location.icontains(location)
    ]
    if params.stars:
        conditions.append(HotelModel.stars == params.stars)
    return await HotelsRepo.get_all(*conditions)
