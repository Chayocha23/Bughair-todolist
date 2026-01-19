"""Unit tests for Task 2: Create and edit to-do-list items functionality."""

import pytest
import tempfile
from pathlib import Path

# Add src to path for imports
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from models import TodoManager, TodoItem, Priority, Status


class TestTodoManager:
    """Test cases for TodoManager class."""

    @pytest.fixture
    def temp_todos_file(self):
        """Create a temporary todos file for testing."""
        with tempfile.NamedTemporaryFile(mode='w+', suffix='.json', delete=False) as f:
            f.write('[]')
            temp_path = Path(f.name)
        yield temp_path
        # Cleanup
        temp_path.unlink(missing_ok=True)

    @pytest.fixture
    def todo_manager(self, temp_todos_file):
        """Create TodoManager instance with temporary file."""
        return TodoManager(temp_todos_file)

    def test_create_todo_basic(self, todo_manager):
        """Test basic todo creation."""
        todo = todo_manager.create_todo(
            title="Test Todo",
            details="Test details",
            priority=Priority.HIGH,
            owner="testuser"
        )

        assert todo.title == "Test Todo"
        assert todo.details == "Test details"
        assert todo.priority == Priority.HIGH
        assert todo.owner == "testuser"
        assert todo.status == Status.PENDING
        assert todo.id is not None

    def test_create_todo_persistence(self, todo_manager):
        """Test that created todos are persisted."""
        todo_manager.create_todo(
            title="Persistent Todo",
            details="Should be saved",
            priority=Priority.MID,
            owner="testuser"
        )

        # Load todos again to verify persistence
        todos = todo_manager.load_todos()
        assert len(todos) == 1
        saved_todo = todos[0]
        assert saved_todo.title == "Persistent Todo"
        assert saved_todo.owner == "testuser"

    def test_get_todos_by_user(self, todo_manager):
        """Test filtering todos by user."""
        # Create todos for different users
        todo_manager.create_todo("User1 Todo1", "Details1", Priority.HIGH, "user1")
        todo_manager.create_todo("User1 Todo2", "Details2", Priority.MID, "user1")
        todo_manager.create_todo("User2 Todo1", "Details3", Priority.LOW, "user2")

        # Get todos for user1
        user1_todos = todo_manager.get_todos_by_user("user1")
        assert len(user1_todos) == 2
        assert all(todo.owner == "user1" for todo in user1_todos)

        # Get todos for user2
        user2_todos = todo_manager.get_todos_by_user("user2")
        assert len(user2_todos) == 1
        assert user2_todos[0].owner == "user2"

    def test_get_todo_by_id(self, todo_manager):
        """Test retrieving todo by ID."""
        todo = todo_manager.create_todo("Find Me", "Details", Priority.HIGH, "testuser")

        # Should find the todo
        found = todo_manager.get_todo_by_id(todo.id)
        assert found is not None
        assert found.id == todo.id
        assert found.title == "Find Me"

        # Should return None for nonexistent ID
        not_found = todo_manager.get_todo_by_id("nonexistent-id")
        assert not_found is None

    def test_update_todo_title(self, todo_manager):
        """Test updating todo title."""
        todo = todo_manager.create_todo("Original Title", "Details", Priority.HIGH, "testuser")

        # Update title
        updated = todo_manager.update_todo(todo.id, title="New Title")

        assert updated is not None
        assert updated.title == "New Title"
        assert updated.details == "Details"  # Unchanged
        assert updated.priority == Priority.HIGH  # Unchanged

    def test_update_todo_details(self, todo_manager):
        """Test updating todo details."""
        todo = todo_manager.create_todo("Title", "Original Details", Priority.HIGH, "testuser")

        # Update details
        updated = todo_manager.update_todo(todo.id, details="New Details")

        assert updated is not None
        assert updated.title == "Title"  # Unchanged
        assert updated.details == "New Details"

    def test_update_todo_priority(self, todo_manager):
        """Test updating todo priority."""
        todo = todo_manager.create_todo("Title", "Details", Priority.LOW, "testuser")

        # Update priority
        updated = todo_manager.update_todo(todo.id, priority=Priority.HIGH)

        assert updated is not None
        assert updated.priority == Priority.HIGH

    def test_update_todo_status(self, todo_manager):
        """Test updating todo status."""
        todo = todo_manager.create_todo("Title", "Details", Priority.HIGH, "testuser")

        # Update status
        updated = todo_manager.update_todo(todo.id, status=Status.COMPLETED)

        assert updated is not None
        assert updated.status == Status.COMPLETED

    def test_update_todo_nonexistent(self, todo_manager):
        """Test updating nonexistent todo returns None."""
        result = todo_manager.update_todo("nonexistent-id", title="New Title")
        assert result is None

    def test_delete_todo_existing(self, todo_manager):
        """Test deleting an existing todo."""
        todo = todo_manager.create_todo("To Delete", "Details", Priority.HIGH, "testuser")

        # Delete should succeed
        result = todo_manager.delete_todo(todo.id)
        assert result is True

        # Todo should no longer exist
        assert todo_manager.get_todo_by_id(todo.id) is None

    def test_delete_todo_nonexistent(self, todo_manager):
        """Test deleting nonexistent todo returns False."""
        result = todo_manager.delete_todo("nonexistent-id")
        assert result is False

    def test_todo_item_to_dict(self):
        """Test TodoItem.to_dict() method."""
        todo = TodoItem(
            title="Test Title",
            details="Test Details",
            priority=Priority.HIGH,
            owner="testuser",
            status=Status.COMPLETED,
            id="test-id",
            created_at="2023-01-01T00:00:00",
            updated_at="2023-01-02T00:00:00"
        )

        todo_dict = todo.to_dict()

        expected = {
            "id": "test-id",
            "title": "Test Title",
            "details": "Test Details",
            "priority": "HIGH",
            "status": "COMPLETED",
            "owner": "testuser",
            "created_at": "2023-01-01T00:00:00",
            "updated_at": "2023-01-02T00:00:00"
        }

        assert todo_dict == expected

    def test_todo_item_from_dict(self):
        """Test TodoItem.from_dict() class method."""
        data = {
            "id": "test-id",
            "title": "Test Title",
            "details": "Test Details",
            "priority": "HIGH",
            "status": "COMPLETED",
            "owner": "testuser",
            "created_at": "2023-01-01T00:00:00",
            "updated_at": "2023-01-02T00:00:00"
        }

        todo = TodoItem.from_dict(data)

        assert todo.id == "test-id"
        assert todo.title == "Test Title"
        assert todo.details == "Test Details"
        assert todo.priority == Priority.HIGH
        assert todo.status == Status.COMPLETED
        assert todo.owner == "testuser"
        assert todo.created_at == "2023-01-01T00:00:00"
        assert todo.updated_at == "2023-01-02T00:00:00"