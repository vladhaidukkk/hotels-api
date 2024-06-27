from fastapi import Request
from pydantic import SecretStr
from sqladmin.authentication import AuthenticationBackend

from app.config import settings
from app.users.auth import authenticate_user, authorize_user, create_access_token
from app.users.enums import Role


class AdminAuthBackend(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username, password = form["username"], form["password"]

        user = await authenticate_user(email=username, password=SecretStr(password))
        if not user or user.role != Role.ADMIN:
            return False

        access_token = create_access_token({"sub": user.id})
        request.session.update({"access_token": access_token})

        return True

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        access_token = request.session.get("access_token")
        if not access_token:
            return False

        user = await authorize_user(access_token)
        if not user:
            return False

        if user.role != Role.ADMIN:
            return False

        return True


auth_backend = AdminAuthBackend(secret_key=settings.jwt_secret_key)
