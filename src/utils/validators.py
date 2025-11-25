import re
from datetime import datetime

class ValidationError(Exception):
    """Custom exception for validation errors."""
    pass

def validate_email(email: str) -> bool:
    """Validates an email address format."""
    if not email:
        raise ValidationError("Email cannot be empty.")
    pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    if not re.match(pattern, email):
        raise ValidationError(f"Invalid email format: {email}")
    return True

def validate_phone(phone: str) -> bool:
    """Validates a phone number (simple 10 digit check)."""
    if not phone:
        raise ValidationError("Phone number cannot be empty.")
    if not phone.isdigit() or len(phone) != 10:
        raise ValidationError(f"Invalid phone number: {phone}. Must be 10 digits.")
    return True

def validate_password(password: str) -> bool:
    """
    Validates password strength.
    Must be at least 8 chars, contain 1 uppercase, 1 lowercase, 1 number.
    """
    if not password:
        raise ValidationError("Password cannot be empty.")
    if len(password) < 8:
        raise ValidationError("Password must be at least 8 characters long.")
    if not any(c.isupper() for c in password):
        raise ValidationError("Password must contain at least one uppercase letter.")
    if not any(c.islower() for c in password):
        raise ValidationError("Password must contain at least one lowercase letter.")
    if not any(c.isdigit() for c in password):
        raise ValidationError("Password must contain at least one number.")
    return True

def validate_amount(amount: float) -> bool:
    """Validates that an amount is positive."""
    if not isinstance(amount, (int, float)):
        raise ValidationError("Amount must be a number.")
    if amount <= 0:
        raise ValidationError("Amount must be positive.")
    return True

def validate_date_format(date_str: str) -> bool:
    """Validates date string format YYYY-MM-DD."""
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        raise ValidationError(f"Invalid date format: {date_str}. Use YYYY-MM-DD.")

def validate_username(username: str) -> bool:
    """
    Validates username requirements:
    - Alphanumeric only
    - Length between 3 and 20 characters
    """
    if not username:
        raise ValidationError("Username cannot be empty.")
    if not 3 <= len(username) <= 20:
        raise ValidationError("Username must be between 3 and 20 characters.")
    if not username.isalnum():
        raise ValidationError("Username must be alphanumeric.")
    return True

def validate_address(address: str) -> bool:
    """
    Validates address (mock complex validation).
    """
    if not address:
        raise ValidationError("Address cannot be empty.")
    if len(address) < 10:
        raise ValidationError("Address is too short.")
    return True

def validate_pin(pin: str) -> bool:
    """Validates a 4-digit PIN."""
    if not pin or len(pin) != 4 or not pin.isdigit():
        raise ValidationError("PIN must be exactly 4 digits.")
    return True

def sanitize_input(input_str: str) -> str:
    """
    Sanitizes input to prevent injection (mock).
    """
    if not input_str:
        return ""
    return input_str.replace("<", "&lt;").replace(">", "&gt;")

