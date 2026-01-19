"""Unit tests for Task 3: Create and edit a to-do-list item."""

import pytest
import tempfile
import json
from pathlib import Path
from datetime import datetime

# Add src to path for imports
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from models import TodoManager, Priority, Status


class TestTodoItemCreation:
    """Test cases for creating todo items."""

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

    def test_create_todo_with_high_priority(self, todo_manager):
        """Test creating a todo with HIGH priority."""
        todo = todo_manager.create_todo(
            title="Urgent Task",
            details="This is an urgent task",
            priority=Priority.HIGH,
            owner="alice"
        )

        assert todo.title == "Urgent Task"
        assert todo.details == "This is an urgent task"
        assert todo.priority == Priority.HIGH
        assert todo.owner == "alice"
        assert todo.status == Status.PENDING

    def test_create_todo_with_mid_priority(self, todo_manager):
        """Test creating a todo with MID priority."""
        todo = todo_manager.create_todo(
            title="Normal Task",
            details="This is a normal priority task",
            priority=Priority.MID,
            owner="bob"
        )

        assert todo.title == "Normal Task"
        assert todo.priority == Priority.MID

    def test_create_todo_with_low_priority(self, todo_manager):
        """Test creating a todo with LOW priority."""
        todo = todo_manager.create_todo(
            title="Low Priority Task",
            details="This can wait",
            priority=Priority.LOW,
            owner="charlie"
        )

        assert todo.title == "Low Priority Task"
        assert todo.priority == Priority.LOW

    def test_created_todo_has_unique_id(self, todo_manager):
        """Test that each created todo has a unique ID."""
        todo1 = todo_manager.create_todo(
            title="Task 1",
            details="First task",
            priority=Priority.HIGH,
            owner="alice"
        )
        todo2 = todo_manager.create_todo(
            title="Task 2",
            details="Second task",
            priority=Priority.MID,
            owner="alice"
        )

        assert todo1.id != todo2.id
        assert todo1.id is not None
        assert todo2.id is not None

    def test_created_todo_has_timestamps(self, todo_manager):
        """Test that created todos have created_at and updated_at timestamps."""
        todo = todo_manager.create_todo(
            title="Timestamped Task",
            details="Task with timestamps",
            priority=Priority.HIGH,
            owner="alice"
        )

        assert todo.created_at is not None
        assert todo.updated_at is not None
        # Verify timestamps are valid ISO-8601 format
        datetime.fromisoformat(todo.created_at)
        datetime.fromisoformat(todo.updated_at)

    def test_todo_created_with_pending_status(self, todo_manager):
        """Test that newly created todos have PENDING status."""
        todo = todo_manager.create_todo(
            title="New Task",
            details="Task details",
            priority=Priority.MID,
            owner="alice"
        )

        assert todo.status == Status.PENDING

    def test_create_multiple_todos(self, todo_manager):
        """Test creating multiple todos for the same user."""
        todo_manager.create_todo(
            title="Task 1",
            details="Details 1",
            priority=Priority.HIGH,
            owner="alice"
        )
        todo_manager.create_todo(
            title="Task 2",
            details="Details 2",
            priority=Priority.MID,
            owner="alice"
        )
        todo_manager.create_todo(
            title="Task 3",
            details="Details 3",
            priority=Priority.LOW,
            owner="alice"
        )

        todos = todo_manager.get_todos_by_user("alice")
        assert len(todos) == 3

    def test_create_todos_for_different_users(self, todo_manager):
        """Test creating todos for different users."""
        todo_manager.create_todo(
            title="Alice Task",
            details="Alice details",
            priority=Priority.HIGH,
            owner="alice"
        )
        todo_manager.create_todo(
            title="Bob Task",
            details="Bob details",
            priority=Priority.MID,
            owner="bob"
        )

        alice_todos = todo_manager.get_todos_by_user("alice")
        bob_todos = todo_manager.get_todos_by_user("bob")

        assert len(alice_todos) == 1
        assert len(bob_todos) == 1
        assert alice_todos[0].owner == "alice"
        assert bob_todos[0].owner == "bob"

    def test_create_todo_persisted_to_file(self, todo_manager):
        """Test that created todos are persisted to the JSON file."""
        todo = todo_manager.create_todo(
            title="Persistent Task",
            details="Task details",
            priority=Priority.HIGH,
            owner="alice"
        )

        # Load todos from file directly
        with open(todo_manager.todos_file, 'r') as f:
            data = json.load(f)

        assert len(data) == 1
        assert data[0]['title'] == "Persistent Task"
        assert data[0]['id'] == todo.id


class TestTodoItemEditing:
    """Test cases for editing todo items."""

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

    def test_edit_todo_title(self, todo_manager):
        """Test editing the title of a todo."""
        todo = todo_manager.create_todo(
            title="Original Title",
            details="Task details",
            priority=Priority.HIGH,
            owner="alice"
        )

        updated_todo = todo_manager.update_todo(
            todo.id,
            title="Updated Title"
        )

        assert updated_todo is not None
        assert updated_todo.title == "Updated Title"
        assert updated_todo.id == todo.id

    def test_edit_todo_details(self, todo_manager):
        """Test editing the details of a todo."""
        todo = todo_manager.create_todo(
            title="Task Title",
            details="Original details",
            priority=Priority.MID,
            owner="alice"
        )

        updated_todo = todo_manager.update_todo(
            todo.id,
            details="Updated details"
        )

        assert updated_todo is not None
        assert updated_todo.details == "Updated details"
        assert updated_todo.title == "Task Title"  # Title unchanged

    def test_edit_todo_priority(self, todo_manager):
        """Test editing the priority of a todo."""
        todo = todo_manager.create_todo(
            title="Task Title",
            details="Task details",
            priority=Priority.LOW,
            owner="alice"
        )

        updated_todo = todo_manager.update_todo(
            todo.id,
            priority=Priority.HIGH
        )

        assert updated_todo is not None
        assert updated_todo.priority == Priority.HIGH

    def test_edit_todo_status(self, todo_manager):
        """Test editing the status of a todo."""
        todo = todo_manager.create_todo(
            title="Task Title",
            details="Task details",
            priority=Priority.MID,
            owner="alice"
        )

        assert todo.status == Status.PENDING

        updated_todo = todo_manager.update_todo(
            todo.id,
            status=Status.COMPLETED
        )

        assert updated_todo is not None
        assert updated_todo.status == Status.COMPLETED

    def test_edit_multiple_fields(self, todo_manager):
        """Test editing multiple fields at once."""
        todo = todo_manager.create_todo(
            title="Original Title",
            details="Original details",
            priority=Priority.LOW,
            owner="alice"
        )

        updated_todo = todo_manager.update_todo(
            todo.id,
            title="New Title",
            details="New details",
            priority=Priority.HIGH,
            status=Status.COMPLETED
        )

        assert updated_todo.title == "New Title"
        assert updated_todo.details == "New details"
        assert updated_todo.priority == Priority.HIGH
        assert updated_todo.status == Status.COMPLETED

    def test_edit_updates_updated_at_timestamp(self, todo_manager):
        """Test that editing a todo updates the updated_at timestamp."""
        todo = todo_manager.create_todo(
            title="Task Title",
            details="Task details",
            priority=Priority.MID,
            owner="alice"
        )

        original_updated_at = todo.updated_at

        updated_todo = todo_manager.update_todo(
            todo.id,
            title="Updated Title"
        )

        assert updated_todo.updated_at >= original_updated_at

    def test_edit_nonexistent_todo_returns_none(self, todo_manager):
        """Test that editing a nonexistent todo returns None."""
        result = todo_manager.update_todo(
            "nonexistent-id",
            title="New Title"
        )

        assert result is None

    def test_edit_todo_persisted_to_file(self, todo_manager):
        """Test that edited todos are persisted to the JSON file."""
        todo = todo_manager.create_todo(
            title="Original Title",
            details="Original details",
            priority=Priority.LOW,
            owner="alice"
        )

        todo_manager.update_todo(
            todo.id,
            title="Updated Title",
            priority=Priority.HIGH
        )

        # Load from file and verify
        with open(todo_manager.todos_file, 'r') as f:
            data = json.load(f)

        assert len(data) == 1
        assert data[0]['title'] == "Updated Title"
        assert data[0]['priority'] == "HIGH"

    def test_edit_preserves_other_fields(self, todo_manager):
        """Test that editing one field preserves other fields."""
        todo = todo_manager.create_todo(
            title="Task Title",
            details="Task details",
            priority=Priority.MID,
            owner="alice"
        )

        original_owner = todo.owner
        original_created_at = todo.created_at

        updated_todo = todo_manager.update_todo(
            todo.id,
            title="New Title"
        )

        assert updated_todo.owner == original_owner
        assert updated_todo.created_at == original_created_at

    def test_edit_only_provided_fields(self, todo_manager):
        """Test that only provided fields are updated."""
        todo = todo_manager.create_todo(
            title="Original Title",
            details="Original details",
            priority=Priority.LOW,
            owner="alice"
        )

        # Update only title, leaving other fields unchanged
        updated_todo = todo_manager.update_todo(todo.id, title="New Title")

        assert updated_todo.title == "New Title"
        assert updated_todo.details == "Original details"
        assert updated_todo.priority == Priority.LOW


class TestCreateEditIntegration:
    """Integration tests for creating and editing todos."""

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

    def test_create_and_edit_workflow(self, todo_manager):
        """Test complete workflow of creating and then editing a todo."""
        # Create a todo
        todo = todo_manager.create_todo(
            title="Buy groceries",
            details="Milk, eggs, bread",
            priority=Priority.MID,
            owner="alice"
        )

        assert todo.title == "Buy groceries"
        assert todo.status == Status.PENDING

        # Edit the todo to update priority
        updated_todo = todo_manager.update_todo(
            todo.id,
            priority=Priority.HIGH
        )

        assert updated_todo.priority == Priority.HIGH

        # Edit again to mark as completed
        final_todo = todo_manager.update_todo(
            updated_todo.id,
            status=Status.COMPLETED
        )

        assert final_todo.status == Status.COMPLETED
        assert final_todo.title == "Buy groceries"
        assert final_todo.priority == Priority.HIGH

    def test_create_multiple_todos_and_edit_specific_one(self, todo_manager):
        """Test creating multiple todos and editing a specific one."""
        # Create three todos
        todo1 = todo_manager.create_todo(
            title="Task 1",
            details="Details 1",
            priority=Priority.HIGH,
            owner="alice"
        )
        todo2 = todo_manager.create_todo(
            title="Task 2",
            details="Details 2",
            priority=Priority.MID,
            owner="alice"
        )
        todo3 = todo_manager.create_todo(
            title="Task 3",
            details="Details 3",
            priority=Priority.LOW,
            owner="alice"
        )

        # Edit only the second todo
        todo_manager.update_todo(
            todo2.id,
            title="Updated Task 2",
            priority=Priority.HIGH
        )

        # Verify only todo2 was edited
        todos = todo_manager.get_todos_by_user("alice")
        assert len(todos) == 3

        for todo in todos:
            if todo.id == todo1.id:
                assert todo.title == "Task 1"
            elif todo.id == todo2.id:
                assert todo.title == "Updated Task 2"
                assert todo.priority == Priority.HIGH
            elif todo.id == todo3.id:
                assert todo.title == "Task 3"

    def test_sequential_edits_to_same_todo(self, todo_manager):
        """Test making multiple sequential edits to the same todo."""
        todo = todo_manager.create_todo(
            title="Original",
            details="Original details",
            priority=Priority.LOW,
            owner="alice"
        )

        # First edit
        todo = todo_manager.update_todo(todo.id, title="First Edit")
        assert todo.title == "First Edit"

        # Second edit
        todo = todo_manager.update_todo(todo.id, details="Updated details")
        assert todo.details == "Updated details"

        # Third edit
        todo = todo_manager.update_todo(todo.id, priority=Priority.HIGH)
        assert todo.priority == Priority.HIGH

        # Verify all changes persisted
        retrieved_todo = todo_manager.get_todo_by_id(todo.id)
        assert retrieved_todo.title == "First Edit"
        assert retrieved_todo.details == "Updated details"
        assert retrieved_todo.priority == Priority.HIGH

    def test_create_edit_with_empty_details(self, todo_manager):
        """Test creating and editing todos with empty details."""
        # Create todo with empty details
        todo = todo_manager.create_todo(
            title="Task",
            details="",
            priority=Priority.MID,
            owner="alice"
        )

        assert todo.details == ""

        # Edit to add details
        updated_todo = todo_manager.update_todo(
            todo.id,
            details="Now with details"
        )

        assert updated_todo.details == "Now with details"
