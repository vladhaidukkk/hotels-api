from typing import Annotated

import jwt
from fastapi import Cookie, HTTPException, status
from jwt import InvalidTokenError

from app.config import settings
from app.users.model import UserModel
from app.users.repo import UsersRepo


async def get_current_user(
    access_token: Annotated[str | None, Cookie()] = None
) -> UserModel:
    if not access_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )

    try:
        payload = jwt.decode(
            access_token, key=settings.jwt_secret_key, algorithms=settings.jwt_algorithm
        )
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )

    # The next two checks are generally redundant, as we don't need to worry about
    # someone sending a self-made token.
    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )

    user = await UsersRepo.get_by_id(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )

    return user
