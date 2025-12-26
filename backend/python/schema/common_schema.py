from pydantic import BaseModel
from typing import Optional, Dict

class SuccessResponseSchema(BaseModel):
    message: str

class ErrorResponseSchema(BaseModel):
    error: str
    details: Optional[Dict] = None