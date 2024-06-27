from typing import Annotated

from fastapi import Cookie, Depends

from app.exceptions import invalid_token
from app.users.auth import authorize_user
from app.users.model import UserModel


async def get_current_user(
    access_token: Annotated[str | None, Cookie()] = None
) -> UserModel:
    if not access_token:
        raise invalid_token

    user = await authorize_user(access_token)
    if not user:
        raise invalid_token

    return user


CurrentUser = Annotated[UserModel, Depends(get_current_user)]
