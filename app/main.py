from contextlib import asynccontextmanager
from typing import AsyncIterator

from fastapi import APIRouter, FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from sqladmin import Admin

from app.admin.auth import auth_backend
from app.admin.views import BookingView, HotelView, RoomView, UserView
from app.bookings.router import router as bookings_router
from app.config import settings
from app.db.core import engine
from app.hotels.router import router as hotels_router
from app.pages.router import router as pages_router
from app.upload.router import router as upload_router
from app.users.router import router as users_router


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    redis = aioredis.from_url(settings.app.redis.url)
    FastAPICache.init(RedisBackend(redis), prefix="cache")
    yield


app = FastAPI(lifespan=lifespan)

app.mount("/static", StaticFiles(directory="app/static"), "static")

api_router = APIRouter(prefix="/api")
api_router.include_router(users_router)
api_router.include_router(hotels_router)
api_router.include_router(bookings_router)

app.include_router(api_router)
app.include_router(pages_router)
app.include_router(upload_router)

admin = Admin(app, engine=engine, authentication_backend=auth_backend)

admin.add_view(UserView)
admin.add_view(HotelView)
admin.add_view(RoomView)
admin.add_view(BookingView)
