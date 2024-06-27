from app.users.repo import UsersRepo
from app.users.enums import Role
from datetime import date


async def test_add_user():
    email = "test@example.com"
    hashed_password = "a1b2c3d4e5"
    role = Role.USER

    result = await UsersRepo.add(
        email=email, hashed_password=hashed_password, role=role
    )

    assert result.id == 1
    assert result.email == email
    assert result.hashed_password == hashed_password
    assert result.role == role
    assert isinstance(result.created_at, date)
    assert isinstance(result.updated_at, date)
