from core.adapters.db.base_db import BaseDB
from core.logger import Logger
from aiofile import AIOFile
import json
import os
from typing import List, Optional

logger = Logger.get_logger(__name__)

class JsonFileDB(BaseDB):
    def __init__(self, data_dir: str = "data"):
        """Initialize the JSON file database adapter."""
        self.data_dir = data_dir
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)
            logger.info(f"Created data directory: {self.data_dir}")

    async def initialize(self):
        """Initialize the database (if needed)."""
        logger.info("JsonFileDB initialized.")

    async def cleanup(self):
        """Cleanup resources (if needed)."""
        logger.info("JsonFileDB cleaned up.")

    async def _read_json_content_from_file(self, file_path: str) -> dict:
        """Read JSON content from a file."""
        logger.debug(f"Reading JSON content from file: {file_path}")
        try:
            if not os.path.exists(file_path):
                logger.warning(f"File does not exist: {file_path}")
                return {}
            async with AIOFile(file_path, 'r') as afp:
                content = await afp.read()
                return json.loads(content) if content else {}
        except FileNotFoundError:
            logger.warning(f"File not found: {file_path}")
            return {}
        except json.JSONDecodeError as e:
            logger.error(f"Failed to decode JSON from file: {file_path}. Error: {e}")
            return {}
        except Exception as e:
            logger.error(f"Unexpected error while reading file: {file_path}. Error: {e}")
            return {}

    async def _write_json_content_to_file(self, file_path: str, content: dict):
        """Write JSON content to a file."""
        logger.debug(f"Writing JSON content to file: {file_path}")
        try:
            async with AIOFile(file_path, 'w') as afp:
                await afp.write(json.dumps(content, indent=4))
        except Exception as e:
            logger.error(f"Failed to write JSON to file: {file_path}. Error: {e}")
            raise

    async def create_record(self, collection: str, data: dict) -> dict:
        """Create a new record in the specified collection."""
        logger.debug(f"Creating record in collection: {collection} with data: {data}")
        collection_file_path = os.path.join(self.data_dir, f"{collection}.json")
        try:
            existing_content = await self._read_json_content_from_file(collection_file_path)
            records = existing_content.get("records", [])
            records.append(data)
            await self._write_json_content_to_file(collection_file_path, {"records": records})
            logger.info(f"Record created successfully in collection: {collection}")
            return data
        except Exception as e:
            logger.error(f"Failed to create record in collection: {collection}. Error: {e}")
            raise

    async def get_all_records(self, collection: str) -> List[dict]:
        """Retrieve all records from the specified collection."""
        logger.debug(f"Retrieving all records from collection: {collection}")
        collection_file_path = os.path.join(self.data_dir, f"{collection}.json")
        try:
            existing_content = await self._read_json_content_from_file(collection_file_path)
            return existing_content.get("records", [])
        except Exception as e:
            logger.error(f"Failed to retrieve records from collection: {collection}. Error: {e}")
            raise

    async def get_record_by_id(self, collection: str, record_id: str) -> Optional[dict]:
        """Retrieve a record by its ID from the specified collection."""
        logger.debug(f"Retrieving record by ID: {record_id} from collection: {collection}")
        collection_file_path = os.path.join(self.data_dir, f"{collection}.json")
        try:
            existing_content = await self._read_json_content_from_file(collection_file_path)
            records = existing_content.get("records", [])
            for record in records:
                if record.get("id") == record_id:
                    logger.info(f"Record found with ID: {record_id}")
                    return record
            logger.warning(f"Record with ID: {record_id} not found in collection: {collection}")
            return None
        except Exception as e:
            logger.error(f"Failed to retrieve record by ID: {record_id}. Error: {e}")
            raise

    async def update_record(self, collection: str, record_id: str, data: dict) -> Optional[dict]:
        """Update a record by its ID in the specified collection."""
        logger.debug(f"Updating record by ID: {record_id} in collection: {collection} with data: {data}")
        collection_file_path = os.path.join(self.data_dir, f"{collection}.json")
        try:
            existing_content = await self._read_json_content_from_file(collection_file_path)
            records = existing_content.get("records", [])
            for i, record in enumerate(records):
                if record.get("id") == record_id:
                    for k, v in data.items():
                        if v is not None:
                            record[k] = v
                    records[i] = record
                    await self._write_json_content_to_file(collection_file_path, {"records": records})
                    logger.info(f"Record updated successfully with ID: {record_id}")
                    return record
            logger.warning(f"Record with ID: {record_id} not found in collection: {collection}")
            return None
        except Exception as e:
            logger.error(f"Failed to update record by ID: {record_id}. Error: {e}")
            raise

    async def delete_record(self, collection: str, record_id: str) -> bool:
        """Delete a record by its ID from the specified collection."""
        logger.debug(f"Deleting record by ID: {record_id} from collection: {collection}")
        collection_file_path = os.path.join(self.data_dir, f"{collection}.json")
        try:
            existing_content = await self._read_json_content_from_file(collection_file_path)
            records = existing_content.get("records", [])
            for i, record in enumerate(records):
                if record.get("id") == record_id:
                    records.pop(i)
                    await self._write_json_content_to_file(collection_file_path, {"records": records})
                    logger.info(f"Record deleted successfully with ID: {record_id}")
                    return True
            logger.warning(f"Record with ID: {record_id} not found in collection: {collection}")
            return False
        except Exception as e:
            logger.error(f"Failed to delete record by ID: {record_id}. Error: {e}")
            raise