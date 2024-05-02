from fastapi import FastAPI

from app.bookings import router as bookings_router
from app.hotels.endpoints import router as hotels_router
from app.login import router as login_router

app = FastAPI()


app.include_router(hotels_router)
app.include_router(bookings_router)
app.include_router(login_router)
