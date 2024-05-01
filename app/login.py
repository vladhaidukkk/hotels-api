from typing import Annotated

from fastapi import APIRouter, Form
from fastapi.responses import HTMLResponse
from pydantic import EmailStr, SecretStr

from app.pages import Page, read_page

router = APIRouter(prefix="/login", tags=["Login"])


@router.get("")
def login_page():
    login_page_content = read_page(Page.LOGIN)
    return HTMLResponse(login_page_content)


@router.post("")
def login(email: Annotated[EmailStr, Form()], password: Annotated[SecretStr, Form()]):
    welcome_page_template = read_page(Page.WELCOME)
    welcome_page_content = welcome_page_template.replace("{{email}}", email)
    return HTMLResponse(welcome_page_content)
