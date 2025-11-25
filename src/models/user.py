from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime
import hashlib
from src.utils.validators import validate_email, validate_phone

@dataclass
class User:
    user_id: str
    username: str
    password_hash: str
    email: str
    phone: str
    is_admin: bool = False
    created_at: datetime = field(default_factory=datetime.now)
    accounts: List[str] = field(default_factory=list)  # List of Account IDs

    def __post_init__(self):
        # basic validation on init
        validate_email(self.email)
        validate_phone(self.phone)

    @staticmethod
    def hash_password(password: str) -> str:
        """Hashes a password using SHA-256."""
        return hashlib.sha256(password.encode()).hexdigest()

    def verify_password(self, password: str) -> bool:
        """Verifies a password against the stored hash."""
        return self.hash_password(password) == self.password_hash

    def add_account(self, account_id: str):
        if account_id not in self.accounts:
            self.accounts.append(account_id)

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "username": self.username,
            "password_hash": self.password_hash,
            "email": self.email,
            "phone": self.phone,
            "is_admin": self.is_admin,
            "created_at": self.created_at.isoformat(),
            "accounts": self.accounts
        }

    @classmethod
    def from_dict(cls, data):
        user = cls(
            user_id=data["user_id"],
            username=data["username"],
            password_hash=data["password_hash"],
            email=data["email"],
            phone=data["phone"],
            is_admin=data["is_admin"],
            accounts=data.get("accounts", [])
        )
        user.created_at = datetime.fromisoformat(data["created_at"])
        return user
