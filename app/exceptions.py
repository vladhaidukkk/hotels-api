from fastapi import HTTPException, status

user_already_exists = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="User with this email already exists",
)

invalid_credentials = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
)

invalid_token = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
)
