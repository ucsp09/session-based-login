from fastapi import APIRouter, Response, status, Depends
from schema.user_schema import CreateUserRequestSchema, UpdateUserRequestSchema, CreateUserResponseSchema, GetUserResponseSchema, GetAllUsersResponseSchema
from schema.common_schema import ErrorResponseSchema, SuccessResponseSchema
from utils import user_utils, uuid_utils
from dao.user_dao import UserDao
from core.bootstrap import get_user_dao
from core.logger import Logger

user_api_router = APIRouter()
logger = Logger.get_logger(__name__)

@user_api_router.get("/users/{user_id}")
async def get_user(user_id: str, response: Response, user_dao: UserDao = Depends(get_user_dao)):
    logger.info(f"Received request to get user with user_id: {user_id}")

    if not user_id:
        logger.warning("User ID is missing in the request.")
        response.status_code = status.HTTP_400_BAD_REQUEST
        return ErrorResponseSchema(error="User ID is required.")

    logger.info(f"Fetching user data for user_id: {user_id}")
    user_data, err = await user_dao.get_user(user_id)
    if err:
        logger.error(f"Error occurred while fetching user data for user_id: {user_id}. Error: {err}")
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return ErrorResponseSchema(error="Failed to retrieve user.")
    if not user_data:
        logger.warning(f"User with user_id: {user_id} does not exist.")
        response.status_code = status.HTTP_404_NOT_FOUND
        return ErrorResponseSchema(error="User not found.")

    logger.info(f"Successfully retrieved user data for user_id: {user_id}")
    response.status_code = status.HTTP_200_OK
    return GetUserResponseSchema(userId=user_data["id"], username=user_data["username"], role=user_data["role"])


@user_api_router.post("/users")
async def create_user(input_data: CreateUserRequestSchema, response: Response, user_dao: UserDao = Depends(get_user_dao)):
    logger.info(f"Received request to create a new user with username: {input_data.username}")

    if not user_utils.is_valid_username(input_data.username):
        logger.warning(f"Invalid username format: {input_data.username}")
        response.status_code = status.HTTP_400_BAD_REQUEST
        return ErrorResponseSchema(error="Invalid username format.")

    if not user_utils.is_valid_password(input_data.password):
        logger.warning("Invalid password format.")
        response.status_code = status.HTTP_400_BAD_REQUEST
        return ErrorResponseSchema(error="Invalid password format.")

    if not user_utils.is_built_in_role(input_data.role):
        logger.warning(f"Invalid role specified: {input_data.role}")
        response.status_code = status.HTTP_400_BAD_REQUEST
        return ErrorResponseSchema(error="Invalid role specified.")

    user_data, err = await user_dao.get_user_by_username(input_data.username)
    if err:
        logger.error(f"Error occurred while checking existing user with username: {input_data.username}. Error: {err}")
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return ErrorResponseSchema(error="Failed to create user.")
    if user_data:
        logger.warning(f"User with username: {input_data.username} already exists.")
        response.status_code = status.HTTP_409_CONFLICT
        return ErrorResponseSchema(error="Username already exists.")

    logger.info(f"Creating user with username: {input_data.username}")
    user_data = input_data.dict()
    user_data['id'] = uuid_utils.generate_uuid()
    user_data['password'] = user_utils.get_hashed_password(input_data.password)

    _, err = await user_dao.create_user(user_data=user_data)
    if err:
        logger.error(f"Failed to create user with username: {input_data.username}. Error: {err}")
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return ErrorResponseSchema(error="Failed to create user.")

    logger.info(f"User created successfully with username: {input_data.username}")
    response.status_code = status.HTTP_201_CREATED
    return CreateUserResponseSchema(userId=user_data['id'], username=input_data.username, role=input_data.role)


@user_api_router.put("/users/{user_id}")
async def update_user(user_id: str, input_data: UpdateUserRequestSchema, response: Response, user_dao: UserDao = Depends(get_user_dao)):
    logger.info(f"Received request to update user with user_id: {user_id}")

    if not user_id:
        logger.warning("User ID is missing in the request.")
        response.status_code = status.HTTP_400_BAD_REQUEST
        return ErrorResponseSchema(error="User ID is required.")

    user_data, err = await user_dao.get_user(user_id)
    if err:
        logger.error(f"Error occurred while fetching user data for user_id: {user_id}. Error: {err}")
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return ErrorResponseSchema(error="Failed to update user.")
    if not user_data:
        logger.warning(f"User with user_id: {user_id} does not exist.")
        response.status_code = status.HTTP_404_NOT_FOUND
        return ErrorResponseSchema(error="User not found.")

    update_data = input_data.dict(exclude_unset=True)
    if "password" in update_data and not user_utils.is_valid_password(update_data["password"]):
        logger.warning("Invalid password format in update request.")
        response.status_code = status.HTTP_400_BAD_REQUEST
        return ErrorResponseSchema(error="Invalid password format.")

    if "role" in update_data and not user_utils.is_built_in_role(update_data["role"]):
        logger.warning(f"Invalid role specified in update request: {update_data['role']}")
        response.status_code = status.HTTP_400_BAD_REQUEST
        return ErrorResponseSchema(error="Invalid role specified.")

    if "password" in update_data:
        update_data["password"] = user_utils.get_hashed_password(update_data["password"])

    logger.info(f"Updating user with user_id: {user_id}")
    updated_user_data, err = await user_dao.update_user(user_id, update_data)
    if err:
        logger.error(f"Failed to update user with user_id: {user_id}. Error: {err}")
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return ErrorResponseSchema(error="Failed to update user.")

    logger.info(f"User updated successfully with user_id: {user_id}")
    response.status_code = status.HTTP_200_OK
    return GetUserResponseSchema(userId=updated_user_data["id"], username=updated_user_data["username"], role=updated_user_data["role"])


@user_api_router.delete("/users/{user_id}")
async def delete_user(user_id: str, response: Response, user_dao: UserDao = Depends(get_user_dao)):
    logger.info(f"Received request to delete user with user_id: {user_id}")

    if not user_id:
        logger.warning("User ID is missing in the request.")
        response.status_code = status.HTTP_400_BAD_REQUEST
        return ErrorResponseSchema(error="User ID is required.")

    user_data, err = await user_dao.get_user(user_id)
    if err:
        logger.error(f"Error occurred while fetching user data for user_id: {user_id}. Error: {err}")
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return ErrorResponseSchema(error="Failed to delete user.")
    if not user_data:
        logger.warning(f"User with user_id: {user_id} does not exist.")
        response.status_code = status.HTTP_404_NOT_FOUND
        return ErrorResponseSchema(error="User not found.")

    logger.info(f"Deleting user with user_id: {user_id}")
    success, err = await user_dao.delete_user(user_id)
    if err or not success:
        logger.error(f"Failed to delete user with user_id: {user_id}. Error: {err}")
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return ErrorResponseSchema(error="Failed to delete user.")

    logger.info(f"User deleted successfully with user_id: {user_id}")
    response.status_code = status.HTTP_200_OK
    return SuccessResponseSchema(message="User deleted successfully.")


@user_api_router.get("/users")
async def get_all_users(response: Response, user_dao: UserDao = Depends(get_user_dao)):
    logger.info("Received request to fetch all users.")

    users, err = await user_dao.get_all_users()
    if err:
        logger.error(f"Failed to retrieve users. Error: {err}")
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return ErrorResponseSchema(error="Failed to retrieve users.")

    logger.info(f"Successfully retrieved {len(users)} users.")
    response.status_code = status.HTTP_200_OK
    return GetAllUsersResponseSchema(items=[GetUserResponseSchema(userId=user["id"], username=user["username"], role=user["role"]) for user in users], total=len(users))
