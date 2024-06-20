from typing import Annotated

import jwt
from fastapi import Cookie, Depends
from jwt import InvalidTokenError

from app.config import settings
from app.exceptions import invalid_token
from app.users.model import UserModel
from app.users.repo import UsersRepo


async def get_current_user(
    access_token: Annotated[str | None, Cookie()] = None
) -> UserModel:
    if not access_token:
        raise invalid_token

    try:
        payload = jwt.decode(
            access_token, key=settings.jwt_secret_key, algorithms=settings.jwt_algorithm
        )
    except InvalidTokenError:
        raise invalid_token

    # The next two checks are generally redundant, as we don't need to worry about
    # someone sending a self-made token.
    user_id = payload.get("sub")
    if not user_id:
        raise invalid_token

    user = await UsersRepo.get_by_id(user_id)
    if not user:
        raise invalid_token

    return user


CurrentUser = Annotated[UserModel, Depends(get_current_user)]
