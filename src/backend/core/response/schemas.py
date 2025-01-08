from pydantic import BaseModel


class ErrorMessageSchema(BaseModel):
    message: str
