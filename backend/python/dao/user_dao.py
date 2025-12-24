from typing import Any, Tuple, List, Dict, Optional
from adapters.db.base_db import BaseDB

class UserDao:
    def __init__(self, db: BaseDB):
        self.db = db
        self.collection = "users"

    async def create_user(self, user_data: dict) -> Tuple[Optional[Dict], Any]:
        # Logic to create a user in the database
        try:
            user = await self.db.create_record(self.collection, user_data)
            return user, None
        except Exception as e:
            return None, e

    async def get_user(self, user_id: str) -> Tuple[Optional[Dict], Any]:
        # Logic to retrieve a user from the database
        try:
            user = await self.db.get_record_by_id(self.collection, user_id)
            if user:
                return user, None
            else:
                return None, "User not found"
        except Exception as e:
            return None, e

    async def update_user(self, user_id: str, update_data: dict) -> Tuple[Optional[Dict], Any]:
        # Logic to update a user in the database
        try:
            updated_user = await self.db.update_record(self.collection, user_id, update_data)
            if updated_user:
                return updated_user, None
            else:
                return None, "User not found"
        except Exception as e:
            return None, e

    async def delete_user(self, user_id: str) -> Tuple[bool, Any]:
        # Logic to delete a user from the database
        try:
            success = await self.db.delete_record(self.collection, user_id)
            return success, None
        except Exception as e:
            return False, e

    async def get_all_users(self) -> Tuple[List[Dict], Any]:
        # Logic to retrieve all users from the database
        try:
            users = await self.db.get_all_records(self.collection)
            return users, None
        except Exception as e:
            return [], e

    async def user_exists(self, username: str) -> Tuple[bool, Any]:
        # Logic to check if a user exists in the database
        try:
            users = await self.db.get_all_records(self.collection)
            for user in users:
                if user.get("username") == username:
                    return True, None
            return False, None
        except Exception as e:
            return False, e

    async def get_user_by_username(self, username: str) -> Tuple[Optional[Dict], Any]:
        # Logic to retrieve a user by username from the database
        try:
            users = await self.db.get_all_records(self.collection)
            for user in users:
                if user.get("username") == username:
                    return user, None
            return None, "User not found"
        except Exception as e:
            return None, e