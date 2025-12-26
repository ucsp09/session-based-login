import time
from core.logger import Logger

logger = Logger.get_logger(__name__)

def is_session_valid(expires_at: float) -> bool:
    """Check if the session is still valid based on the expiration timestamp."""
    logger.debug(f"Checking session validity. Expires at: {expires_at}, Current time: {time.monotonic()}")
    if time.monotonic() >= expires_at:
        return False
    return True

def get_session_expiration_timestamp(duration_seconds: int) -> float:
    """Get the expiration timestamp for a session given a duration in seconds."""
    logger.debug(f"Calculating session expiration timestamp with duration: {duration_seconds} seconds.")
    return time.monotonic() + duration_seconds
