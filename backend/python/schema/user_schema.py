from pydantic import BaseModel
from typing import Optional, List

class CreateUserRequestSchema(BaseModel):
    username: str
    password: str
    role: str

class UpdateUserRequestSchema(BaseModel):
    password: Optional[str] = None
    role: Optional[str] = None

class CreateUserResponseSchema(BaseModel):
    userId: str
    username: str
    role: str

class GetUserResponseSchema(BaseModel):
    userId: str
    username: str
    role: str

class GetAllUsersResponseSchema(BaseModel):
    items: List[GetUserResponseSchema]
    total: int

