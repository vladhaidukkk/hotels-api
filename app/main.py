import asyncio
import time

from fastapi import FastAPI

app = FastAPI()


async def get_first_arg():
    print("get_first_arg(): Start")
    await asyncio.sleep(3)
    print("get_first_arg(): End")
    return 1


async def get_second_arg():
    print("get_second_arg(): Start")
    await asyncio.sleep(3)
    print("get_second_arg(): End")
    return 2


@app.get("/")
async def index():
    start = time.perf_counter()
    first_arg_task = asyncio.create_task(get_first_arg())
    second_arg_task = asyncio.create_task(get_second_arg())
    first_arg = await first_arg_task
    second_arg = await second_arg_task
    elapsed = time.perf_counter() - start
    print(f"Execution time: {elapsed:0.2f}")
    return {"first_arg": first_arg, "second_arg": second_arg}
