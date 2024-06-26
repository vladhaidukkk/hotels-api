from sqladmin import ModelView

from app.bookings.model import BookingModel
from app.users.model import UserModel


class UserView(ModelView, model=UserModel):
    name = "User"
    name_plural = "Users"
    icon = "fa-solid fa-user"

    column_exclude_list = [UserModel.hashed_password]
    column_details_exclude_list = [UserModel.hashed_password]


class BookingView(ModelView, model=BookingModel):
    name = "Booking"
    name_plural = "Bookings"
    icon = "fa-solid fa-ticket"

    column_list = "__all__"
