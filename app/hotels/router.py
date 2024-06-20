from typing import Annotated

from fastapi import APIRouter, Query
from sqlalchemy.sql import ColumnExpressionArgument

from app.exceptions import hotel_not_found
from app.hotels.model import HotelModel
from app.hotels.repo import HotelsRepo
from app.hotels.schemas import HotelOut
from app.rooms.router import router as rooms_router
from app.validation.date_range import DateRangeQueryParams

router = APIRouter(prefix="/hotels", tags=["Hotels"])

router.include_router(rooms_router)


@router.get("/{location}", response_model=list[HotelOut])
async def get_hotels(
    location: str,
    date_range: DateRangeQueryParams,
    stars: Annotated[int | None, Query(ge=1, le=5)] = None,
):
    conditions: list[ColumnExpressionArgument[bool]] = [
        HotelModel.location.icontains(location)
    ]
    if stars:
        conditions.append(HotelModel.stars == stars)
    return await HotelsRepo.get_all(*conditions)


@router.get("/id/{hotel_id}", response_model=HotelOut)
async def get_hotel(hotel_id: int) -> HotelModel:
    hotel = await HotelsRepo.get_by_id(hotel_id)
    if not hotel:
        raise hotel_not_found

    return hotel
