from datetime import date
from typing import TypedDict

from pydantic import EmailStr

from app.users.enums import Role
from app.users.model import UserModel


class UserExpected(TypedDict):
    email: EmailStr
    hashed_password: str
    role: Role


def assert_user(user: UserModel, expected: UserExpected) -> None:
    assert isinstance(user.id, int)
    assert user.email == expected["email"]
    assert user.hashed_password == expected["hashed_password"]
    assert user.role == expected["role"]
    assert isinstance(user.created_at, date)
    assert isinstance(user.updated_at, date)
