from abc import ABC, abstractmethod

class BaseSessionStore(ABC):
    @abstractmethod
    async def initialize(self) -> None:
        """Initialize the session store."""
        pass

    @abstractmethod
    async def cleanup(self) -> None:
        """Cleanup the session store."""
        pass

    @abstractmethod
    async def insert_session(self, session_id: str, data: dict) -> None:
        """Insert a new session into the session store."""
        pass

    @abstractmethod
    async def get_session(self, session_id: str) -> dict | None:
        """Retrieve a session from the session store by its ID."""
        pass

    @abstractmethod
    async def delete_session(self, session_id: str) -> None:
        """Delete a session from the session store by its ID."""
        pass

    @abstractmethod
    async def clear_sessions(self) -> None:
        """Clear all sessions from the session store."""
        pass