from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, SecretStr

from app.users.enums import Role


class UserAuth(BaseModel):
    email: EmailStr
    password: SecretStr


class User(BaseModel):
    id: int
    email: EmailStr
    hashed_password: str
    role: Role
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserOut(BaseModel):
    id: int
    email: EmailStr
    role: Role
    created_at: datetime
    updated_at: datetime
