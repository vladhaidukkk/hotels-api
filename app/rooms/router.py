from datetime import date
from typing import Annotated, Self

from fastapi import APIRouter, Depends
from pydantic import BaseModel, model_validator

from app.exceptions import hotel_not_found
from app.hotels.repo import HotelsRepo
from app.rooms.model import RoomModel
from app.rooms.repo import RoomsRepo
from app.rooms.schemas import RoomWithRoomsLeftOut
from app.validation import create_custom_error, raise_request_validation_error

router = APIRouter(prefix="/{hotel_id}/rooms", tags=["Rooms"])


class RoomSearchParams(BaseModel):
    date_from: date | None = None
    date_to: date | None = None


class ValidatedRoomSearchParams(RoomSearchParams):
    @model_validator(mode="after")
    def validate_date_range(self) -> Self:
        if self.date_from and self.date_to and self.date_from > self.date_to:
            raise create_custom_error(
                "date_range_invalid",
                "Start date can't be greater than end date",
            )
        return self


@router.get("", response_model=list[RoomWithRoomsLeftOut])
async def get_rooms(
    hotel_id: int, params: Annotated[RoomSearchParams, Depends()]
) -> list[dict]:
    with raise_request_validation_error("query"):
        ValidatedRoomSearchParams.model_validate(params.model_dump())

    hotel = await HotelsRepo.get_by_id(hotel_id)
    if not hotel:
        raise hotel_not_found

    return await RoomsRepo.get_all_with_rooms_left(RoomModel.hotel_id == hotel_id)
