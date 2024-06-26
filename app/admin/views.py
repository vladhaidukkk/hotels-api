from sqladmin import ModelView

from app.users.model import UserModel


class UserView(ModelView, model=UserModel):
    name = "User"
    name_plural = "Users"
    icon = "fa-solid fa-user"

    column_exclude_list = [UserModel.hashed_password]
    column_details_exclude_list = [UserModel.hashed_password]
