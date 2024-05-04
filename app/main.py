from fastapi import FastAPI

from app.bookings.endpoints import router as bookings_router
from app.hotels.endpoints import router as hotels_router
from app.users.endpoints import router as users_router

app = FastAPI()


app.include_router(users_router)
app.include_router(hotels_router)
app.include_router(bookings_router)
