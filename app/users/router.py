from datetime import datetime

from fastapi import APIRouter, HTTPException, status
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr, SecretStr

from app.users.model import UserModel
from app.users.repo import UsersRepo

router = APIRouter(prefix="/users", tags=["Users"])


class HashService:
    def __init__(self):
        self.context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def hash(self, secret: str) -> str:
        return self.context.hash(secret)


hash_service = HashService()


class UserRegister(BaseModel):
    email: EmailStr
    password: SecretStr


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def create_user(data: UserRegister) -> int:
    existing_user = await UsersRepo.get_one_or_none(UserModel.email == data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists",
        )

    hashed_password = hash_service.hash(data.password.get_secret_value())
    return await UsersRepo.add(email=data.email, hashed_password=hashed_password)
