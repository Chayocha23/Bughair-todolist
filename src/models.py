"""Data models for the CLI To-Do List Application."""

from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
from uuid import uuid4


class Priority(Enum):
    """Priority levels for todo items."""
    HIGH = "HIGH"
    MID = "MID"
    LOW = "LOW"


class Status(Enum):
    """Status states for todo items."""
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"


@dataclass
class TodoItem:
    """Represents a single todo item."""
    title: str
    details: str
    priority: Priority
    owner: str
    status: Status = Status.PENDING
    id: str = field(default_factory=lambda: str(uuid4()))
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> dict:
        """Convert TodoItem to a dictionary."""
        return {
            "id": self.id,
            "title": self.title,
            "details": self.details,
            "priority": self.priority.value,
            "status": self.status.value,
            "owner": self.owner,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "TodoItem":
        """Create a TodoItem from a dictionary."""
        return cls(
            id=data.get("id", str(uuid4())),
            title=data["title"],
            details=data["details"],
            priority=Priority(data["priority"]),
            status=Status(data["status"]),
            owner=data["owner"],
            created_at=data.get("created_at", datetime.now().isoformat()),
            updated_at=data.get("updated_at", datetime.now().isoformat()),
        )
