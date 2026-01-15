"""Data models for the CLI To-Do List Application."""

import json
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
from uuid import uuid4
from pathlib import Path
from typing import Optional, List


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


class TodoManager:
    """Manages todo items - create, read, update, delete operations."""

    def __init__(self, todos_file: Path):
        self.todos_file = todos_file

    def load_todos(self) -> List[TodoItem]:
        """Load todos from JSON file."""
        if not self.todos_file.exists():
            return []
        with open(self.todos_file, "r") as f:
            data = json.load(f)
            return [TodoItem.from_dict(item) for item in data]

    def save_todos(self, todos: List[TodoItem]):
        """Save todos to JSON file."""
        with open(self.todos_file, "w") as f:
            json.dump([todo.to_dict() for todo in todos], f, indent=2)

    def create_todo(
        self, title: str, details: str, priority: Priority, owner: str
    ) -> TodoItem:
        """Create a new todo item."""
        todo = TodoItem(title=title, details=details, priority=priority, owner=owner)
        todos = self.load_todos()
        todos.append(todo)
        self.save_todos(todos)
        return todo

    def get_todos_by_user(self, username: str) -> List[TodoItem]:
        """Get all todos for a specific user."""
        todos = self.load_todos()
        return [todo for todo in todos if todo.owner == username]

    def get_todo_by_id(self, todo_id: str) -> Optional[TodoItem]:
        """Get a specific todo by ID."""
        todos = self.load_todos()
        for todo in todos:
            if todo.id == todo_id:
                return todo
        return None

    def update_todo(
        self,
        todo_id: str,
        title: Optional[str] = None,
        details: Optional[str] = None,
        priority: Optional[Priority] = None,
        status: Optional[Status] = None,
    ) -> Optional[TodoItem]:
        """Update an existing todo item."""
        todos = self.load_todos()
        for i, todo in enumerate(todos):
            if todo.id == todo_id:
                # Update fields if provided
                if title is not None:
                    todo.title = title
                if details is not None:
                    todo.details = details
                if priority is not None:
                    todo.priority = priority
                if status is not None:
                    todo.status = status
                # Always update the updated_at timestamp
                todo.updated_at = datetime.now().isoformat()
                todos[i] = todo
                self.save_todos(todos)
                return todo
        return None

    def delete_todo(self, todo_id: str) -> bool:
        """Delete a todo item."""
        todos = self.load_todos()
        original_length = len(todos)
        todos = [todo for todo in todos if todo.id != todo_id]
        if len(todos) < original_length:
            self.save_todos(todos)
            return True
        return False
