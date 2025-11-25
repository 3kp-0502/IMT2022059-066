import uuid
from typing import Optional
from src.models.user import User
from src.services.audit_service import AuditService
from src.utils.persistence import PersistenceLayer
from src.utils.validators import ValidationError

class AuthService:
    def __init__(self, persistence: PersistenceLayer):
        self.persistence = persistence
        self.audit_service = AuditService()
        self.current_user: Optional[User] = None

    def register(self, username, password, email, phone, is_admin=False) -> User:
        if self.persistence.get_user_by_username(username):
            raise ValidationError(f"Username '{username}' is already taken.")
        
        user_id = str(uuid.uuid4())
        password_hash = User.hash_password(password)
        
        user = User(
            user_id=user_id,
            username=username,
            password_hash=password_hash,
            email=email,
            phone=phone,
            is_admin=is_admin
        )
        
        self.persistence.save_user(user.to_dict())
        self.audit_service.log_action(user.user_id, "REGISTER", f"Username: {username}")
        return user

    def login(self, username, password) -> User:
        user_data = self.persistence.get_user_by_username(username)
        if not user_data:
            raise ValidationError("Invalid username or password.")
        
        user = User.from_dict(user_data)
        if not user.verify_password(password):
            raise ValidationError("Invalid username or password.")
        
        self.current_user = user
        self.audit_service.log_action(user.user_id, "LOGIN", "Success")
        return user

    def logout(self):
        if self.current_user:
            self.audit_service.log_action(self.current_user.user_id, "LOGOUT", "Success")
        self.current_user = None

    def is_authenticated(self) -> bool:
        return self.current_user is not None

    def is_admin(self) -> bool:
        return self.current_user and self.current_user.is_admin
