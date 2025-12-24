from adapters.db.base_db import BaseDB
from aiofile import AIOFile
import json
import os

class JsonFileDB(BaseDB):
    def __init__(self):
        pass

    async def initialize(self):
        pass   

    async def cleanup(self):
        pass

    async def _read_json_content_from_file(self, file_path: str) -> dict:
        async with AIOFile(file_path, 'r') as afp:
            content = await afp.read()
            return json.loads(content) if content else {}
        
    async def _write_json_content_to_file(self, file_path: str, content: dict):
        async with AIOFile(file_path, 'w') as afp:
            await afp.write(json.dumps(content, indent=4))

    async def create_record(self, collection: str, data: dict) -> dict:
        """Create a new record in the specified collection."""
        collection_file_path = f"{collection}.json"
        if os.path.exists(collection_file_path):
            existing_content = await self._read_json_content_from_file(collection_file_path)
            records = existing_content.get("records", [])
        else:
            records = []
        records.append(data)
        await self._write_json_content_to_file(collection_file_path, {"records": records})
    
    async def get_all_records(self, collection: str) -> list[dict]:
        """Retrieve all records from the specified collection."""
        collection_file_path = f"{collection}.json"
        if not os.path.exists(collection_file_path):
            return []
        existing_content = await self._read_json_content_from_file(collection_file_path)
        return existing_content.get("records", [])
    
    async def get_record_by_id(self, collection: str, record_id: str) -> dict | None:
        """Retrieve a record by its ID from the specified collection."""
        collection_file_path = f"{collection}.json"
        if not os.path.exists(collection_file_path):
            return None
        existing_content = await self._read_json_content_from_file(collection_file_path)
        records = existing_content.get("records", [])
        for record in records:
            if record.get("id") == record_id:
                return record
        return None
    
    async def update_record(self, collection: str, record_id: str, data: dict) -> dict | None:
        """Update a record by its ID in the specified collection."""
        collection_file_path = f"{collection}.json"
        if not os.path.exists(collection_file_path):
            return None
        existing_content = await self._read_json_content_from_file(collection_file_path)
        records = existing_content.get("records", [])
        for i, record in enumerate(records):
            if record.get("id") == record_id:
                for k, v in data.items():
                    if v is not None:
                        record[k] = v
                records[i] = record
                await self._write_json_content_to_file(collection_file_path, {"records": records})
                return record
        return None            
    
    async def delete_record(self, collection: str, record_id: str) -> bool:
        """Delete a record by its ID from the specified collection."""
        collection_file_path = f"{collection}.json"
        if not os.path.exists(collection_file_path):
            return False
        existing_content = await self._read_json_content_from_file(collection_file_path)
        records = existing_content.get("records", [])
        for i, record in enumerate(records):
            if record.get("id") == record_id:
                records.pop(i)
                await self._write_json_content_to_file(collection_file_path, {"records": records})
                return True
        return False
    