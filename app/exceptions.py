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

hotel_not_found = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Hotel with this ID doesn't exist",
)

booking_not_found = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Booking with this ID doesn't exist",
)

room_not_found = HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Room with this ID doesn't exist",
)

unavailable_room = HTTPException(
    status_code=status.HTTP_409_CONFLICT,
    detail="Room with this ID is not available during this period",
)
