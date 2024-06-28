from datetime import datetime
from typing import TypedDict

from pydantic import EmailStr

from app.users.enums import Role
from app.users.model import UserModel
from app.users.schemas import UserOut


class UserModelExpected(TypedDict):
    email: EmailStr
    hashed_password: str
    role: Role


def assert_user_model(model: UserModel, expected: UserModelExpected) -> None:
    assert isinstance(model.id, int)
    assert model.email == expected["email"]
    assert model.hashed_password == expected["hashed_password"]
    assert model.role == expected["role"]
    assert isinstance(model.created_at, datetime)
    assert isinstance(model.updated_at, datetime)


class UserOutExpected(TypedDict):
    email: EmailStr
    role: Role


def assert_user_out_dict(dict_: dict, expected: UserOutExpected) -> None:
    user_out = UserOut(**dict_)
    assert user_out.email == expected["email"]
    assert user_out.role == expected["role"]
