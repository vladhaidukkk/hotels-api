from datetime import datetime, timedelta, timezone

import jwt
from fastapi import APIRouter, HTTPException, Response, status
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr, SecretStr

from app.config import settings
from app.users.model import UserModel
from app.users.repo import UsersRepo

router = APIRouter(prefix="/users", tags=["Users"])


class HashService:
    def __init__(self):
        self.context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def hash(self, secret: str) -> str:
        return self.context.hash(secret)

    def verify(self, secret: str, hashed: str) -> bool:
        return self.context.verify(secret, hashed)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    to_encode["exp"] = datetime.now(timezone.utc) + timedelta(
        minutes=settings.jwt_access_token_expire_minutes
    )
    return jwt.encode(
        payload=to_encode, key=settings.jwt_secret_key, algorithm=settings.jwt_algorithm
    )


hash_service = HashService()


class UserAuth(BaseModel):
    email: EmailStr
    password: SecretStr


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(data: UserAuth) -> int:
    existing_user = await UsersRepo.get_one_or_none(UserModel.email == data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists",
        )

    hashed_password = hash_service.hash(data.password.get_secret_value())
    return await UsersRepo.add(email=data.email, hashed_password=hashed_password)


async def authenticate_user(email: EmailStr, password: SecretStr) -> UserModel | None:
    existing_user = await UsersRepo.get_one_or_none(UserModel.email == email)
    if not existing_user:
        return None

    password_is_valid = hash_service.verify(
        password.get_secret_value(), existing_user.hashed_password
    )
    if not password_is_valid:
        return None

    return existing_user


@router.post("/login", status_code=status.HTTP_201_CREATED)
async def login_user(response: Response, data: UserAuth) -> None:
    user = await authenticate_user(data.email, data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )

    access_token = create_access_token({"sub": user.id})
    response.set_cookie("access_token", access_token)
