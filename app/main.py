import time
from contextlib import asynccontextmanager
from typing import AsyncIterator

import sentry_sdk
from fastapi import APIRouter, FastAPI, Request
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
from app.logger import logger
from app.pages.router import router as pages_router
from app.upload.router import router as upload_router
from app.users.router import router as users_router

if settings.app.sentry.dsn and settings.app.sentry.enabled:
    sentry_sdk.init(
        dsn=settings.app.sentry.dsn,
        traces_sample_rate=1.0,
        profiles_sample_rate=1.0,
    )


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    logger.info("lifespan startup")
    redis = aioredis.from_url(settings.app.redis.url)
    FastAPICache.init(RedisBackend(redis), prefix="cache")
    yield
    logger.info("lifespan shutdown")


app = FastAPI(lifespan=lifespan)


@app.middleware("http")
async def log_request_context(request: Request, call_next):
    start_time = time.perf_counter()
    logger.info(
        "start processing %s %s",
        request.method,
        request.url.path,
        extra={
            "method": request.method,
            "url_path": request.url.path,
        },
    )
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    logger.info(
        "finish processing %s %s %s",
        request.method,
        request.url.path,
        response.status_code,
        extra={
            "method": request.method,
            "url_path": request.url.path,
            "status_code": response.status_code,
            "process_time": process_time,
        },
    )
    return response


app.mount("/static", StaticFiles(directory="app/static"), "static")

api_router = APIRouter(prefix="/api/v1")
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
