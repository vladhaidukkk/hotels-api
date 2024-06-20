from datetime import datetime

from pydantic import BaseModel, EmailStr, SecretStr


class UserAuth(BaseModel):
    email: EmailStr
    password: SecretStr


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    updated_at: datetime
