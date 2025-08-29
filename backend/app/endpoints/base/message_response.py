from pydantic import BaseModel


class MessageResponse(BaseModel):
    """
    Represents a response message structure for API communication.

    Args:
        BaseModel: Inherits from Pydantic's BaseModel for data validation.

    Returns:
        An instance containing response message data.
    """

    message: str

    def __call__(self):
        return {"message": self.message}
