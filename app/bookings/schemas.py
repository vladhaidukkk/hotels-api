from datetime import date, datetime

from pydantic import BaseModel


class BookingBase(BaseModel):
    room_id: int
    date_from: date
    date_to: date


class BookingIn(BookingBase):
    pass


class BookingOut(BookingBase):
    id: int
    user_id: int
    price: int
    total_days: int
    total_cost: int
    created_at: datetime
    updated_at: datetime
