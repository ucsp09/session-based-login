from abc import ABC, abstractmethod
from typing import List, Dict, Optional

class BaseDB(ABC):
    """
    Abstract base class for database operations.
    This class defines the interface that all database adapters must implement.
    """

    @abstractmethod
    async def initialize(self):
        """Initialize the connections to the database."""
        pass

    @abstractmethod
    async def cleanup(self):
        """Cleanup the connections to the database."""
        pass

    @abstractmethod
    async def create_record(self, collection: str, data: dict) -> Dict:
        """
        Create a new record in the specified collection.

        Args:
            collection (str): The name of the collection.
            data (dict): The data to be inserted as a record.

        Returns:
            Dict: The created record.
        """
        pass

    @abstractmethod
    async def get_all_records(self, collection: str) -> List[Dict]:
        """
        Retrieve all records from the specified collection.

        Args:
            collection (str): The name of the collection.

        Returns:
            List[Dict]: A list of all records in the collection.
        """
        pass

    @abstractmethod
    async def get_record_by_id(self, collection: str, record_id: str) -> Optional[Dict]:
        """
        Retrieve a record by its ID from the specified collection.

        Args:
            collection (str): The name of the collection.
            record_id (str): The ID of the record to retrieve.

        Returns:
            Optional[Dict]: The record if found, otherwise None.
        """
        pass

    @abstractmethod
    async def update_record(self, collection: str, record_id: str, data: dict) -> Optional[Dict]:
        """
        Update a record by its ID in the specified collection.

        Args:
            collection (str): The name of the collection.
            record_id (str): The ID of the record to update.
            data (dict): The data to update the record with.

        Returns:
            Optional[Dict]: The updated record if found, otherwise None.
        """
        pass

    @abstractmethod
    async def delete_record(self, collection: str, record_id: str) -> bool:
        """
        Delete a record by its ID from the specified collection.

        Args:
            collection (str): The name of the collection.
            record_id (str): The ID of the record to delete.

        Returns:
            bool: True if the record was deleted, False otherwise.
        """
        pass