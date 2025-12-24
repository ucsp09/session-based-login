from fastapi import APIRouter, Response, status
from schema.user_schema import CreateUserRequestSchema, UpdateUserRequestSchema, CreateUserResponseSchema, GetUserResponseSchema, GetAllUsersResponseSchema
from schema.common_schema import ErrorResponseSchema
from utils import user_utils
from dao.user_dao import UserDao

user_api_router = APIRouter()

@user_api_router.get("/users/{user_id}")
async def get_user(user_id: str, response: Response):
    if not user_id:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return ErrorResponseSchema(message="User ID is required.")
    if not UserDao.user_exists(user_id):
        response.status_code = status.HTTP_404_NOT_FOUND
        return ErrorResponseSchema(message="User not found.")
    user_data, err = await UserDao().get_user(user_id)
    if err:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return ErrorResponseSchema(message="Failed to retrieve user.")
    response.status_code = status.HTTP_200_OK
    return GetUserResponseSchema(user_id=user_data["user_id"], username=user_data["username"], role=user_data["role"])


@user_api_router.post("/users")
async def create_user(input_data: CreateUserRequestSchema, response: Response):
    if not user_utils.is_valid_username(input_data.username):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return ErrorResponseSchema(message="Invalid username format.")
    if not user_utils.is_valid_password(input_data.password):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return ErrorResponseSchema(message="Invalid password format.")
    if not user_utils.is_built_in_role(input_data.role):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return ErrorResponseSchema(message="Invalid role specified.")
    if await UserDao().user_exists(input_data.username):
        response.status_code = status.HTTP_409_CONFLICT
        return ErrorResponseSchema(message="Username already exists.")
    user_id, err = await UserDao().create_user(input_data.dict())
    if err:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return ErrorResponseSchema(message="Failed to create user.")
    response.status_code = status.HTTP_201_CREATED
    return CreateUserResponseSchema(user_id=user_id, username=input_data.username, role=input_data.role)
    

@user_api_router.put("/users/{user_id}")
async def update_user(user_id: str, input_data: UpdateUserRequestSchema, response: Response):
    if not user_id:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return ErrorResponseSchema(message="User ID is required.")
    if not await UserDao().user_exists(user_id):
        response.status_code = status.HTTP_404_NOT_FOUND
        return ErrorResponseSchema(message="User not found.")
    update_data = input_data.dict(exclude_unset=True)
    if "password" in update_data and not user_utils.is_valid_password(update_data["password"]):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return ErrorResponseSchema(message="Invalid password format.")
    if "role" in update_data and not user_utils.is_built_in_role(update_data["role"]):
        response.status_code = status.HTTP_400_BAD_REQUEST
        return ErrorResponseSchema(message="Invalid role specified.")
    updated_user_data, err = await UserDao().update_user(user_id, update_data)
    if err:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return ErrorResponseSchema(message="Failed to update user.")
    response.status_code = status.HTTP_200_OK
    return GetUserResponseSchema(user_id=updated_user_data["user_id"], username=updated_user_data["username"], role=updated_user_data["role"])

@user_api_router.delete("/users/{user_id}")
async def delete_user(user_id: str, response: Response):
    if not user_id:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return ErrorResponseSchema(message="User ID is required.")
    if not await UserDao().user_exists(user_id):
        response.status_code = status.HTTP_404_NOT_FOUND
        return ErrorResponseSchema(message="User not found.")
    success, err = await UserDao().delete_user(user_id)
    if err or not success:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return ErrorResponseSchema(message="Failed to delete user.")
    response.status_code = status.HTTP_204_NO_CONTENT

@user_api_router.get("/users")
async def get_all_users(response: Response):
    users, err = await UserDao().get_all_users()
    if err:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return ErrorResponseSchema(message="Failed to retrieve users.")
    response.status_code = status.HTTP_200_OK
    return GetAllUsersResponseSchema(items=[GetUserResponseSchema(user_id=user["user_id"], username=user["username"], role=user["role"]) for user in users], total=len(users))
