from fastapi import APIRouter, Response, Request, status
from schema.common_schema import ErrorResponseSchema
from schema.login_schema import LoginRequestSchema, LoginResponseSchema, LogoutResponseSchema
from utils import user_utils, uuid_utils
from dao.user_dao import UserDao
from core.bootstrap import get_session_store
from config.constants import SESSION_EXPIRY_SECONDS
from datetime import datetime, timedelta

login_api_router = APIRouter()

@login_api_router.post("/login")
async def login(input_data: LoginRequestSchema, request: Request, response: Response):
    session_id =  request.cookies.get("session_id")
    if session_id:
        existing_session = await get_session_store().get_session(session_id)
        if existing_session:
            expiry_time = datetime.fromisoformat(existing_session["expiry"])
            if datetime.utcnow() < expiry_time:
                response.status_code = status.HTTP_200_OK
                return LoginResponseSchema(message="Already logged in.", session_id=session_id)
            else:
                await get_session_store().delete_session(session_id)
    if not user_utils.is_valid_username(input_data.username) or not user_utils.is_valid_password(input_data.password):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return ErrorResponseSchema(message="Invalid username or password format.")
    user_data, err = await UserDao().authenticate_user(input_data.username, input_data.password)
    if err:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return ErrorResponseSchema(message="Authentication failed due to server error.")
    if not user_data:
        response.status_code = status.HTTP_401_UNAUTHORIZED
        return ErrorResponseSchema(message="Invalid username or password.")
    session_id = uuid_utils.generate_uuid()
    expiry = (datetime.utcnow() + timedelta(seconds=SESSION_EXPIRY_SECONDS)).isoformat()
    await get_session_store().insert_session(
        session_id, {"username": user_data["username"], "role": user_data["role"], "expiry": expiry})
    response.status_code = status.HTTP_200_OK
    response.set_cookie(key="session_id", value=session_id, httponly=True, max_age=SESSION_EXPIRY_SECONDS)
    return LoginResponseSchema(message="Login successful.", session_id=session_id)
    

@login_api_router.get("/logout")
async def logout(request: Request, response: Response):
    session_id = request.cookies.get("session_id")
    if not session_id:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return ErrorResponseSchema(message="No active session found.")
    existing_session = await get_session_store().get_session(session_id)
    if not existing_session:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return ErrorResponseSchema(message="No active session found.")
    if existing_session.get("expiry"):
        expiry_time = datetime.fromisoformat(existing_session["expiry"])
        if datetime.utcnow() > expiry_time:
            response.status_code = status.HTTP_400_BAD_REQUEST
            await get_session_store().delete_session(session_id)
            return ErrorResponseSchema(message="Session has already expired.")
    await get_session_store().delete_session(session_id)
    response.status_code = status.HTTP_200_OK
    response.delete_cookie(key="session_id")
    return LogoutResponseSchema(message="Logout successful.")