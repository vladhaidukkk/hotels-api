from datetime import date

import pytest

from app.users.enums import Role
from app.users.repo import UsersRepo
from tests.assertion_helpers.user import assert_user_model


@pytest.mark.db
async def test_add_user():
    email = "test@example.com"
    hashed_password = "a1b2c3d4e5"
    role = Role.USER

    result = await UsersRepo.add(
        email=email, hashed_password=hashed_password, role=role
    )

    assert_user_model(
        result,
        {
            "email": "dd",
            "hashed_password": hashed_password,
            "role": role,
        },
    )


@pytest.mark.db
async def test_add_user_default_role():
    email = "test@example.com"
    hashed_password = "a1b2c3d4e5"

    result = await UsersRepo.add(email=email, hashed_password=hashed_password)

    assert_user_model(
        result,
        {
            "email": email,
            "hashed_password": hashed_password,
            "role": Role.USER,
        },
    )
