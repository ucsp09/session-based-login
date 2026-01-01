from pydantic import BaseModel

class LoginRequestSchema(BaseModel):
    username: str
    password: str

class LoginResponseSchema(BaseModel):
    message: str

class LoginStatusResponseSchema(BaseModel):
    is_logged_in: bool

class LogoutResponseSchema(BaseModel):
    message: str