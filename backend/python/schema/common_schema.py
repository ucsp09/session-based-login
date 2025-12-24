from pydantic import BaseModel

class SuccessResponseSchema(BaseModel):
    message: str

class ErrorResponseSchema(BaseModel):
    error: str
    details: str | None = None