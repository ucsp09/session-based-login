from core.adapters.session_store.base_session_store import BaseSessionStore
from core.logger import Logger
from aiofile import AIOFile
from config.constants import SESSION_STORE_JSON_FILE_PATH
import json
import os
from typing import Dict, Optional

logger = Logger.get_logger(__name__)

class JsonFileSessionStore(BaseSessionStore):
    def __init__(self):
        """Initialize the JSON file session store."""
        if not os.path.exists(SESSION_STORE_JSON_FILE_PATH):
            # Create an empty session file if it doesn't exist
            with open(SESSION_STORE_JSON_FILE_PATH, 'w') as f:
                json.dump({}, f)
            logger.info(f"Created session store file: {SESSION_STORE_JSON_FILE_PATH}")

    async def initialize(self) -> None:
        """Initialize the session store (if needed)."""
        logger.info("JsonFileSessionStore initialized.")

    async def cleanup(self) -> None:
        """Cleanup resources (if needed)."""
        logger.info("JsonFileSessionStore cleaned up.")

    async def _read_sessions_from_file(self) -> Dict:
        """Read sessions from the JSON file."""
        logger.debug(f"Reading sessions from file: {SESSION_STORE_JSON_FILE_PATH}")
        try:
            if not os.path.exists(SESSION_STORE_JSON_FILE_PATH):
                logger.warning(f"Session store file does not exist: {SESSION_STORE_JSON_FILE_PATH}")
                return {}
            async with AIOFile(SESSION_STORE_JSON_FILE_PATH, 'r') as afp:
                content = await afp.read()
                return json.loads(content) if content else {}
        except FileNotFoundError:
            logger.warning(f"Session store file not found: {SESSION_STORE_JSON_FILE_PATH}")
            return {}
        except json.JSONDecodeError as e:
            logger.error(f"Failed to decode JSON from session store file: {SESSION_STORE_JSON_FILE_PATH}. Error: {e}")
            return {}
        except Exception as e:
            logger.error(f"Unexpected error while reading session store file: {SESSION_STORE_JSON_FILE_PATH}. Error: {e}")
            return {}

    async def _write_sessions_to_file(self, sessions: Dict) -> None:
        """Write sessions to the JSON file."""
        logger.debug(f"Writing sessions to file: {SESSION_STORE_JSON_FILE_PATH}")
        try:
            async with AIOFile(SESSION_STORE_JSON_FILE_PATH, 'w') as afp:
                await afp.write(json.dumps(sessions, indent=4))
        except Exception as e:
            logger.error(f"Failed to write sessions to file: {SESSION_STORE_JSON_FILE_PATH}. Error: {e}")
            raise

    async def create_session(self, session_id: str, data: Dict) -> None:
        """Create a new session."""
        logger.debug(f"Creating session with ID: {session_id}")
        try:
            existing_sessions = await self._read_sessions_from_file()
            existing_sessions[session_id] = data
            await self._write_sessions_to_file(existing_sessions)
            logger.info(f"Session created successfully with ID: {session_id}")
        except Exception as e:
            logger.error(f"Failed to create session with ID: {session_id}. Error: {e}")
            raise

    async def get_session(self, session_id: str) -> Optional[Dict]:
        """Retrieve a session by its ID."""
        logger.debug(f"Retrieving session with ID: {session_id}")
        try:
            existing_sessions = await self._read_sessions_from_file()
            session = existing_sessions.get(session_id)
            if session:
                logger.info(f"Session retrieved successfully with ID: {session_id}")
            else:
                logger.warning(f"Session with ID: {session_id} not found")
            return session
        except Exception as e:
            logger.error(f"Failed to retrieve session with ID: {session_id}. Error: {e}")
            raise

    async def delete_session(self, session_id: str) -> None:
        """Delete a session by its ID."""
        logger.debug(f"Deleting session with ID: {session_id}")
        try:
            existing_sessions = await self._read_sessions_from_file()
            if session_id in existing_sessions:
                del existing_sessions[session_id]
                await self._write_sessions_to_file(existing_sessions)
                logger.info(f"Session deleted successfully with ID: {session_id}")
            else:
                logger.warning(f"Session with ID: {session_id} not found")
        except Exception as e:
            logger.error(f"Failed to delete session with ID: {session_id}. Error: {e}")
            raise

    async def clear_sessions(self) -> None:
        """Clear all sessions."""
        logger.debug("Clearing all sessions")
        try:
            await self._write_sessions_to_file({})
            logger.info("All sessions cleared successfully")
        except Exception as e:
            logger.error(f"Failed to clear all sessions. Error: {e}")
            raise