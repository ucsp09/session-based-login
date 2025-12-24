from adapters.session_store.base_session_store import BaseSessionStore
from aiofile import AIOFile
from config.constants import SESSION_STORE_JSON_FILE_PATH
import json

class JsonFileSessionStore(BaseSessionStore):
    def __init__(self):
        pass

    async def initialize(self) -> None:
        pass

    async def cleanup(self) -> None:
        pass

    async def _read_sessions_from_file(self) -> dict:
        async with AIOFile(SESSION_STORE_JSON_FILE_PATH, 'r') as afp:
            content = await afp.read()
            return json.loads(content) if content else {}

    async def _write_sessions_to_file(self, sessions: dict) -> None:
        async with AIOFile(SESSION_STORE_JSON_FILE_PATH, 'w') as afp:
            await afp.write(json.dumps(sessions, indent=4))

    async def create_session(self, session_id: str, data: dict) -> None:
        existing_sessions = await self._read_sessions_from_file()
        existing_sessions[session_id] = data
        await self._write_sessions_to_file(existing_sessions)

    async def get_session(self, session_id: str) -> dict | None:
        existing_sessions = await self._read_sessions_from_file()
        return existing_sessions.get(session_id)

    async def delete_session(self, session_id: str) -> None:
        existing_sessions = await self._read_sessions_from_file()
        if session_id in existing_sessions:
            del existing_sessions[session_id]
            await self._write_sessions_to_file(existing_sessions)

    async def clear_sessions(self) -> None:
        await self._write_sessions_to_file({})