from typing import Any, Tuple, List, Dict, Optional
from core.adapters.db.base_db import BaseDB
from core.logger import Logger

logger = Logger.get_logger(__name__)

class UserDao:
    def __init__(self, db: BaseDB):
        self.db = db
        self.collection = "users"

    async def create_user(self, user_data: dict) -> Tuple[Optional[Dict], Any]:
        """Create a user in the database."""
        try:
            logger.info(f"Creating user with data: {user_data}")
            user = await self.db.create_record(self.collection, user_data)
            logger.info(f"User created successfully with ID: {user.get('id')}")
            return user, None
        except Exception as e:
            logger.error(f"Error creating user: {e}")
            return None, e

    async def get_user(self, user_id: str) -> Tuple[Optional[Dict], Any]:
        """Retrieve a user by ID from the database."""
        try:
            logger.info(f"Retrieving user with ID: {user_id}")
            user = await self.db.get_record_by_id(self.collection, user_id)
            if user:
                logger.info(f"User retrieved successfully with ID: {user_id}")
                return user, None
            else:
                logger.warning(f"User not found with ID: {user_id}")
                return None, None
        except Exception as e:
            logger.error(f"Error retrieving user with ID: {user_id}. Error: {e}")
            return None, e

    async def update_user(self, user_id: str, update_data: dict) -> Tuple[Optional[Dict], Any]:
        """Update a user in the database."""
        try:
            logger.info(f"Updating user with ID: {user_id} with data: {update_data}")
            updated_user = await self.db.update_record(self.collection, user_id, update_data)
            if updated_user:
                logger.info(f"User updated successfully with ID: {user_id}")
                return updated_user, None
            else:
                logger.warning(f"User not found with ID: {user_id}")
                return None, "User not found"
        except Exception as e:
            logger.error(f"Error updating user with ID: {user_id}. Error: {e}")
            return None, e

    async def delete_user(self, user_id: str) -> Tuple[bool, Any]:
        """Delete a user from the database."""
        try:
            logger.info(f"Deleting user with ID: {user_id}")
            success = await self.db.delete_record(self.collection, user_id)
            if success:
                logger.info(f"User deleted successfully with ID: {user_id}")
                return True, None
            else:
                logger.warning(f"User not found with ID: {user_id}")
                return False, "User not found"
        except Exception as e:
            logger.error(f"Error deleting user with ID: {user_id}. Error: {e}")
            return False, e

    async def get_all_users(self) -> Tuple[List[Dict], Any]:
        """Retrieve all users from the database."""
        try:
            logger.info("Retrieving all users")
            users = await self.db.get_all_records(self.collection)
            logger.info(f"Successfully retrieved {len(users)} users")
            return users, None
        except Exception as e:
            logger.error(f"Error retrieving all users. Error: {e}")
            return [], e

    async def get_user_by_username(self, username: str) -> Tuple[Optional[Dict], Any]:
        """Retrieve a user by username from the database."""
        try:
            logger.info(f"Retrieving user with username: {username}")
            users = await self.db.get_all_records(self.collection)
            for user in users:
                if user.get("username") == username:
                    logger.info(f"User retrieved successfully with username: {username}")
                    return user, None
            logger.warning(f"User not found with username: {username}")
            return None, None
        except Exception as e:
            logger.error(f"Error retrieving user with username: {username}. Error: {e}")
            return None, e