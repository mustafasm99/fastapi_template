from fastapi import Response, status
from pydantic import BaseModel


class MessageResponse(BaseModel):
    message: str

    def __init__(self, **data):
        super().__init__(**data) 

    def __call__(self, response: Response):
        response.status_code = status.HTTP_200_OK
        return {"message": self.message}