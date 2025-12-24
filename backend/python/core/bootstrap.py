from adapters.db.base_db import BaseDB
from adapters.db.json_file_db import JsonFileDB
from adapters.session_store.base_session_store import BaseSessionStore
from adapters.session_store.json_file_session_store import JsonFileSessionStore
from config.constants import DB_TYPE, SESSION_STORE_TYPE
from fastapi import Depends
from dao.user_dao import UserDao

# ---- Module-level variables ----
_db: BaseDB | None = None
_session_store: BaseSessionStore | None = None

# ---- Factories ----
def _create_db() -> BaseDB:
    """Factory function to create the appropriate DB instance based on configuration."""
    if DB_TYPE == "json_file":
        return JsonFileDB()
    else:
        raise ValueError(f"Unsupported DB_TYPE: {DB_TYPE}")

def _create_session_store() -> BaseSessionStore:
    """Factory function to create the appropriate Session Store instance based on configuration."""
    if SESSION_STORE_TYPE == "json_file":
        return JsonFileSessionStore()
    else:
        raise ValueError(f"Unsupported SESSION_STORE_TYPE: {SESSION_STORE_TYPE}")

# ---- Accessor Functions ----
def get_db() -> BaseDB:
    """Get the initialized DB instance."""
    global _db
    return _db

def get_session_store() -> BaseSessionStore:
    """Get the initialized Session Store instance."""
    global _session_store
    return _session_store

def get_user_dao(db: BaseDB = Depends(get_db)) -> UserDao:
    """Get an instance of UserDao with the provided DB dependency."""
    return UserDao(db)

# ---- Initialization and Cleanup ----
async def startup_event_handler():
    """Initialize the core components during the app startup."""
    global _db, _session_store
    _db = _create_db()
    await _db.initialize()
    _session_store = _create_session_store()
    await _session_store.initialize()

async def shutdown_event_handler():
    """Cleanup the core components during the app shutdown."""
    global _db, _session_store
    if _db is not None:
        await _db.cleanup()
        _db = None
    if _session_store is not None:
        await _session_store.cleanup()
        _session_store = None
