from pydantic import BaseModel

class CreateUserRequestSchema(BaseModel):
    username: str
    password: str
    role: str

class UpdateUserRequestSchema(BaseModel):
    password: str | None = None
    role: str | None = None

class CreateUserResponseSchema(BaseModel):
    user_id: str
    username: str
    role: str

class GetUserResponseSchema(BaseModel):
    user_id: str
    username: str
    role: str

class GetAllUsersResponseSchema(BaseModel):
    items: list[GetUserResponseSchema]
    total: int

