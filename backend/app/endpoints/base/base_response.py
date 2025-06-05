from typing import Generic, TypeVar, Optional
from pydantic import BaseModel


T = TypeVar('T')

class BaseResponse(BaseModel, Generic[T]):
    message: str
    data: Optional[T]


class TokenResponse(BaseModel):
    access_token: str
    token_type: str

