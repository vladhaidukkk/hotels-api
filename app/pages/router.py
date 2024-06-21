from typing import Annotated

from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates

from app.hotels.router import get_hotels

router = APIRouter(tags=["Pages"])

templates = Jinja2Templates(directory="app/templates")


@router.get("/hotels")
def get_hotels_page(
    request: Request,
    hotels: Annotated[list[dict], Depends(get_hotels)],
):
    return templates.TemplateResponse(
        name="hotels.jinja", request=request, context={"hotels": hotels}
    )
