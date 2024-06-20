from fastapi import APIRouter

from app.exceptions import hotel_not_found
from app.hotels.repo import HotelsRepo
from app.rooms.model import RoomModel
from app.rooms.repo import RoomsRepo
from app.rooms.schemas import RoomOut

router = APIRouter(prefix="/{hotel_id}/rooms", tags=["Rooms"])


@router.get("", response_model=list[RoomOut])
async def get_rooms(hotel_id: int) -> list[RoomModel]:
    hotel = await HotelsRepo.get_by_id(hotel_id)
    if not hotel:
        raise hotel_not_found

    return await RoomsRepo.get_all(RoomModel.hotel_id == hotel_id)
