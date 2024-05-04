from datetime import datetime

from fastapi import APIRouter, HTTPException, status
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr, SecretStr
from sqlalchemy.exc import IntegrityError

from app.db.core import session_factory
from app.users.model import UserModel

router = APIRouter(prefix="/users", tags=["Users"])


class HashService:
    def __init__(self):
        self.context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def hash(self, secret: str) -> str:
        return self.context.hash(secret)


hash_service = HashService()


class UserIn(BaseModel):
    email: EmailStr
    password: SecretStr


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    updated_at: datetime


@router.post("", status_code=status.HTTP_201_CREATED, response_model=UserOut)
async def create_user(data: UserIn):
    async with session_factory() as session:
        try:
            hashed_password = hash_service.hash(data.password.get_secret_value())
            user = UserModel(email=data.email, hashed_password=hashed_password)
            session.add(user)
            await session.commit()
        except IntegrityError:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="User with this email already exists",
            )

    return user
