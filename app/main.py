from fastapi import FastAPI

from app.hotels import router as hotels_router
from app.bookings import router as bookings_router

app = FastAPI()

app.include_router(hotels_router)
app.include_router(bookings_router)
