from datetime import datetime, timedelta, timezone

import jwt
from passlib.context import CryptContext
from pydantic import EmailStr, SecretStr

from app.config import settings
from app.users.model import UserModel
from app.users.repo import UsersRepo

context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_secret(secret: str) -> str:
    return context.hash(secret)


def verify_secret(secret: str, hashed: str) -> bool:
    return context.verify(secret, hashed)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    to_encode["exp"] = datetime.now(timezone.utc) + timedelta(
        minutes=settings.jwt_access_token_expire_minutes
    )
    return jwt.encode(
        payload=to_encode, key=settings.jwt_secret_key, algorithm=settings.jwt_algorithm
    )


async def authenticate_user(email: EmailStr, password: SecretStr) -> UserModel | None:
    existing_user = await UsersRepo.get_one_or_none(UserModel.email == email)
    if not existing_user:
        return None

    password_is_valid = verify_secret(
        password.get_secret_value(), existing_user.hashed_password
    )
    if not password_is_valid:
        return None

    return existing_user
