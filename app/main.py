from datetime import date
from typing import Annotated

from fastapi import FastAPI, Query

app = FastAPI()


@app.get("/hotels")
def get_hotels(
        location: str,
        date_from: date,
        date_to: date,
        stars: Annotated[int | None, Query(ge=1, le=5)] = None,
):
    return {
        "location": location,
        "date_from": date_from,
        "date_to": date_to,
        "stars": stars,
    }
