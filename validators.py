import re


def validate_username(username):
    """
    Username rules:
    - 3 to 20 characters
    - Letters, numbers, and underscores only
    - Case-sensitive
    """

    pattern = r"^[A-Za-z0-9_]{3,20}$"
    return re.match(pattern, username) is not None


def validate_email(email):
    """
    Basic email validation using regex.
    """

    pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
    return re.match(pattern, email) is not None


def validate_password_strength(password):
    """
    Password rules:
    - Minimum 8 characters
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one digit
    - At least one special character
    """

    if len(password) < 8:
        return False, "Password must be at least 8 characters long."

    if not re.search(r"[A-Z]", password):
        return False, "Password must contain at least one uppercase letter."

    if not re.search(r"[a-z]", password):
        return False, "Password must contain at least one lowercase letter."

    if not re.search(r"[0-9]", password):
        return False, "Password must contain at least one digit."

    if not re.search(r"[!@#$%^&*(),.?\":{}|<>_\-+=/\\[\];']", password):
        return False, "Password must contain at least one special character."

    return True, "Password is strong."