from config.constants import BUILT_IN_ROLES, MIN_PASSWORD_LENGTH, MAX_PASSWORD_LENGTH, MIN_USERNAME_LENGTH, MAX_USERNAME_LENGTH

def is_valid_username(username: str):
    if len(username) < MIN_USERNAME_LENGTH or len(username) > MAX_USERNAME_LENGTH:
        return False
    return True

def is_valid_password(password: str):
    if len(password) < MIN_PASSWORD_LENGTH or len(password) > MAX_PASSWORD_LENGTH:
        return False
    return True

def is_built_in_role(role: str):
    if role not in BUILT_IN_ROLES:
        return False
    return True
