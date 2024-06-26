from sqladmin import ModelView

from app.bookings.model import BookingModel
from app.hotels.model import HotelModel
from app.rooms.model import RoomModel
from app.users.model import UserModel


class UserView(ModelView, model=UserModel):
    name = "User"
    name_plural = "Users"
    icon = "fa-solid fa-user"

    column_exclude_list = [UserModel.hashed_password]
    column_details_exclude_list = [UserModel.hashed_password]


class HotelView(ModelView, model=HotelModel):
    name = "Hotel"
    name_plural = "Hotels"
    icon = "fa-solid fa-hotel"

    column_list = "__all__"


class RoomView(ModelView, model=RoomModel):
    name = "Room"
    name_plural = "Rooms"
    icon = "fa-solid fa-bed"

    column_list = "__all__"


class BookingView(ModelView, model=BookingModel):
    name = "Booking"
    name_plural = "Bookings"
    icon = "fa-solid fa-ticket"

    column_list = "__all__"
