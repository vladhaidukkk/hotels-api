from contextlib import contextmanager
from typing import Generator, LiteralString

from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from pydantic_core import PydanticCustomError


def create_custom_error(
    error_type: LiteralString, message: LiteralString
) -> PydanticCustomError:
    return PydanticCustomError(error_type, message, {"error": {}})


@contextmanager
def raise_request_validation_error(
    loc: str | None = None,
) -> Generator[None, None, None]:
    try:
        yield
    except ValidationError as err:
        errors = err.errors()
        if loc:
            for error in errors:
                error["loc"] = (loc, *error["loc"])
        raise RequestValidationError(errors)
