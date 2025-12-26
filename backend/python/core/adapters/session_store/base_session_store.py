from abc import ABC, abstractmethod
from typing import Dict, Optional

class BaseSessionStore(ABC):
    """
    Abstract base class for session store operations.
    This class defines the interface that all session store adapters must implement.
    """

    @abstractmethod
    async def initialize(self) -> None:
        """
        Initialize the session store.

        This method is called during the startup phase to prepare the session store.
        """
        pass

    @abstractmethod
    async def cleanup(self) -> None:
        """
        Cleanup the session store.

        This method is called during the shutdown phase to release any resources held by the session store.
        """
        pass

    @abstractmethod
    async def create_session(self, session_id: str, data: dict) -> None:
        """
        Create a new session in the session store.

        Args:
            session_id (str): The unique ID of the session.
            data (dict): The data to be stored in the session.
        """
        pass

    @abstractmethod
    async def get_session(self, session_id: str) -> Optional[Dict]:
        """
        Retrieve a session from the session store by its ID.

        Args:
            session_id (str): The unique ID of the session.

        Returns:
            Optional[Dict]: The session data if found, otherwise None.
        """
        pass

    @abstractmethod
    async def delete_session(self, session_id: str) -> None:
        """
        Delete a session from the session store by its ID.

        Args:
            session_id (str): The unique ID of the session.
        """
        pass

    @abstractmethod
    async def clear_sessions(self) -> None:
        """
        Clear all sessions from the session store.

        This method removes all session data from the session store.
        """
        pass