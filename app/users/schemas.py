from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, SecretStr


class UserAuth(BaseModel):
    email: EmailStr
    password: SecretStr


class User(BaseModel):
    id: int
    email: EmailStr
    hashed_password: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    updated_at: datetime
