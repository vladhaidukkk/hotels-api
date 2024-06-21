from fastapi import APIRouter, FastAPI

from app.bookings.router import router as bookings_router
from app.hotels.router import router as hotels_router
from app.pages.router import router as pages_router
from app.users.router import router as users_router
from app.upload.router import router as upload_router

app = FastAPI()

api_router = APIRouter(prefix="/api")
api_router.include_router(users_router)
api_router.include_router(hotels_router)
api_router.include_router(bookings_router)

app.include_router(api_router)
app.include_router(pages_router)
app.include_router(upload_router)
