from pydantic import BaseModel, Field
from typing import TypeVar, Generic


T = TypeVar("T")


class PaginationResponse(BaseModel, Generic[T]):
    """A generic pagination class for handling paginated API responses.

    Args:
        BaseModel: The base model class for data validation and serialization.
        Generic: Enables type-safe pagination for different data types.
    """

    data: list[T]
    total: int
    page: int
    per_page: int
    total_pages: int


class PaginationInput(BaseModel):
    """A class for handling pagination input parameters.

    Args:
        BaseModel (_type_): The base model class for data validation and serialization.
     Returns:
            PaginationInput: An instance containing pagination parameters.
     Attributes:
            page (int): The current page number, starting from 1.
            per_page (int): The number of items per page, with a maximum limit.
    """

    page: int = Field(1, ge=1)
    per_page: int = Field(10, le=100)
