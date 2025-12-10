from enum import Enum
from datetime import datetime
from typing import Optional


class UserRole(Enum):
    """Enumeration of user roles in the Fantasy F1 application."""
    ADMIN = "admin"
    MANAGER = "manager"
    PLAYER = "player"


class User:
    """User model for the Fantasy F1 application."""
    
    def __init__(
        self,
        id: int,
        username: str,
        email: str,
        password_hash: str,
        role: UserRole = UserRole.PLAYER,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
        is_active: bool = True,
    ):
        """
        Initialize a User instance.
        
        Args:
            id: Unique identifier for the user
            username: Unique username for the user
            email: Email address of the user
            password_hash: Hashed password for the user
            role: User role (default: PLAYER)
            created_at: Timestamp when the user was created
            updated_at: Timestamp when the user was last updated
            is_active: Whether the user account is active
        """
        self.id = id
        self.username = username
        self.email = email
        self.password_hash = password_hash
        self.role = role
        self.created_at = created_at or datetime.utcnow()
        self.updated_at = updated_at or datetime.utcnow()
        self.is_active = is_active
    
    def __repr__(self) -> str:
        """Return a string representation of the User."""
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}', role={self.role.value})>"
    
    def is_admin(self) -> bool:
        """Check if the user has admin role."""
        return self.role == UserRole.ADMIN
    
    def is_manager(self) -> bool:
        """Check if the user has manager role."""
        return self.role == UserRole.MANAGER
    
    def is_player(self) -> bool:
        """Check if the user has player role."""
        return self.role == UserRole.PLAYER
    
    def update_last_modified(self) -> None:
        """Update the updated_at timestamp to current time."""
        self.updated_at = datetime.utcnow()
    
    def activate(self) -> None:
        """Activate the user account."""
        self.is_active = True
        self.update_last_modified()
    
    def deactivate(self) -> None:
        """Deactivate the user account."""
        self.is_active = False
        self.update_last_modified()
    
    def to_dict(self) -> dict:
        """Convert the User instance to a dictionary."""
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "role": self.role.value,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "is_active": self.is_active,
        }
