from pydantic import BaseModel, EmailStr, SecretStr


class UserAuth(BaseModel):
    email: EmailStr
    password: SecretStr
