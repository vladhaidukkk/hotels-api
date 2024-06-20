from fastapi import APIRouter, HTTPException, Response, status

from app.users.auth import authenticate_user, create_access_token, hash_secret
from app.users.deps import CurrentUser
from app.users.model import UserModel
from app.users.repo import UsersRepo
from app.users.schemas import UserAuth, UserOut

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(data: UserAuth) -> int:
    existing_user = await UsersRepo.get_one_or_none(UserModel.email == data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists",
        )

    hashed_password = hash_secret(data.password.get_secret_value())
    return await UsersRepo.add(email=data.email, hashed_password=hashed_password)


@router.post("/login")
async def login_user(response: Response, data: UserAuth) -> None:
    user = await authenticate_user(data.email, data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        )

    access_token = create_access_token({"sub": user.id})
    response.set_cookie("access_token", access_token)


@router.post("/logout")
async def logout_user(response: Response) -> None:
    response.delete_cookie("access_token")


@router.get("/me", response_model=UserOut)
async def get_logged_user(user: CurrentUser) -> UserModel:
    return user
