from datetime import date
from typing import Annotated, Self

from fastapi import Depends
from pydantic import BaseModel, model_validator

from app.validation.utils import (
    create_custom_validation_error,
    raise_request_validation_error,
)


class DateRange(BaseModel):
    date_from: date
    date_to: date


class ValidatedDateRange(DateRange):
    @model_validator(mode="after")
    def validate_date_range(self) -> Self:
        if self.date_from > self.date_to:
            raise create_custom_validation_error(
                "invalid_date_range",
                "Start date can't be greater than end date",
            )
        return self


def get_date_range_query_params(
    date_range: Annotated[DateRange, Depends()]
) -> DateRange:
    with raise_request_validation_error("query"):
        ValidatedDateRange.model_validate(date_range.model_dump())
    return date_range


DateRangeQueryParams = Annotated[DateRange, Depends(get_date_range_query_params)]
