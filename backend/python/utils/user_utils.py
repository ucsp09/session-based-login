from config.constants import BUILT_IN_ROLES, MIN_PASSWORD_LENGTH, MAX_PASSWORD_LENGTH, MIN_USERNAME_LENGTH, MAX_USERNAME_LENGTH
import bcrypt
from core.logger import Logger

logger = Logger.get_logger(__name__)

def is_valid_username(username: str) -> bool:
    """Validate the username based on length constraints."""
    logger.debug(f"Validating username: {username}")
    if len(username) < MIN_USERNAME_LENGTH:
        logger.warning(f"Username validation failed: Length is less than {MIN_USERNAME_LENGTH}.")
        return False
    if len(username) > MAX_USERNAME_LENGTH:
        logger.warning(f"Username validation failed: Length exceeds {MAX_USERNAME_LENGTH}.")
        return False
    logger.info(f"Username validation passed for: {username}")
    return True

def is_valid_password(password: str) -> bool:
    """Validate the password based on length constraints."""
    logger.debug("Validating password.")
    if len(password) < MIN_PASSWORD_LENGTH:
        logger.warning(f"Password validation failed: Length is less than {MIN_PASSWORD_LENGTH}.")
        return False
    if len(password) > MAX_PASSWORD_LENGTH:
        logger.warning(f"Password validation failed: Length exceeds {MAX_PASSWORD_LENGTH}.")
        return False
    logger.info("Password validation passed.")
    return True

def is_built_in_role(role: str) -> bool:
    """Validate if the role is a built-in role."""
    logger.debug(f"Validating role: {role}")
    if role not in BUILT_IN_ROLES:
        logger.warning(f"Role validation failed: {role} is not a built-in role.")
        return False
    logger.info(f"Role validation passed for: {role}")
    return True

def get_hashed_password(password: str) -> str:
    """Hash the password using bcrypt."""
    logger.debug("Hashing password.")
    try:
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        logger.info("Password hashed successfully.")
        return hashed.decode('utf-8')
    except Exception as e:
        logger.error(f"Error hashing password. Error: {e}")
        raise

def verify_password(password: str, hashed_password: str) -> bool:
    """Verify the password against the hashed password."""
    logger.debug("Verifying password.")
    try:
        password_bytes = password.encode('utf-8')
        hashed_password_bytes = hashed_password.encode('utf-8')
        if bcrypt.checkpw(password_bytes, hashed_password_bytes):
            logger.info("Password verification passed.")
            return True
        else:
            logger.warning("Password verification failed.")
            return False
    except Exception as e:
        logger.error(f"Error verifying password. Error: {e}")
        raise