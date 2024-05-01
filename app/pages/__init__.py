from enum import Enum
from functools import cache


class Page(Enum):
    WELCOME = "welcome"
    LOGIN = "login"


@cache
def read_page(page: Page):
    with open(f"app/pages/{page.value}.html") as f:
        return f.read()
