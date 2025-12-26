from uuid import uuid4
from core.logger import Logger

logger = Logger.get_logger(__name__)

def generate_uuid() -> str:
    """Generate a new UUID and return it as a hex string."""
    logger.debug("Generating a new UUID.")
    new_uuid = uuid4().hex
    logger.info(f"Generated UUID: {new_uuid}")
    return new_uuid