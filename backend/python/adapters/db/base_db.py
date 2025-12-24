from abc import ABC, abstractmethod

class BaseDB(ABC):
    @abstractmethod
    async def initialize(self):
        """Initialize the connections to the database."""
        pass

    @abstractmethod
    async def cleanup(self):
        """Cleanup the connections to the database."""
        pass

    @abstractmethod
    async def create_record(self, collection: str, data: dict) -> dict:
        """Create a new record in the specified collection."""
        pass

    @abstractmethod
    async def get_all_records(self, collection: str) -> list[dict]:
        """Retrieve all records from the specified collection."""
        pass

    @abstractmethod
    async def get_record_by_id(self, collection: str, record_id: str) -> dict | None:
        """Retrieve a record by its ID from the specified collection."""
        pass

    @abstractmethod
    async def update_record(self, collection: str, record_id: str, data: dict) -> dict | None:
        """Update a record by its ID in the specified collection."""
        pass

    @abstractmethod
    async def delete_record(self, collection: str, record_id: str) -> bool:
        """Delete a record by its ID from the specified collection."""
        pass
