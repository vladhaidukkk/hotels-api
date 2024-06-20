from typing import Sequence

from fastapi import APIRouter

from app.exceptions import hotel_not_found
from app.hotels.repo import HotelsRepo
from app.rooms.repo import RoomsRepo
from app.rooms.schemas import RoomWithRoomsLeftOut
from app.validation.date_range import DateRangeQueryParams

router = APIRouter(prefix="/{hotel_id}/rooms")


@router.get("", response_model=list[RoomWithRoomsLeftOut])
async def get_rooms(hotel_id: int, date_range: DateRangeQueryParams) -> Sequence[dict]:
    hotel = await HotelsRepo.get_by_id(hotel_id)
    if not hotel:
        raise hotel_not_found

    return await RoomsRepo.get_available_hotel_rooms(
        hotel_id=hotel_id,
        date_from=date_range.date_from,
        date_to=date_range.date_to,
    )
