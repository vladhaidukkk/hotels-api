import asyncio

from fastapi import APIRouter
from prometheus_fastapi_instrumentator import Instrumentator

instrumentator = Instrumentator(
    should_group_status_codes=False,
    excluded_handlers=[".*admin.*", "/metrics"],
)
router = APIRouter(prefix="/metrics")


@router.get("/raise_error")
def raise_error():
    raise RuntimeError


@router.get("/consume_time")
async def consume_time():
    await asyncio.sleep(5)
    return 1


@router.get("/consume_memory")
def get_error():
    _ = [i for i in range(100_000_000)]
    return 1
