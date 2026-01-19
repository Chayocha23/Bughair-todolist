"""Unit tests for Task 4, Task 5, and Task 6 functionality.

Task 4: View all to-do-list items
Task 5: View to-do-list item details
Task 6: Mark a to-do-list item as completed
"""

import pytest
import tempfile
from pathlib import Path
from io import StringIO
import sys

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from models import TodoManager, TodoItem, Priority, Status


class TestTask4ViewAllTodos:
    """Test cases for Task 4: View all to-do-list items."""

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

    def test_get_todos_by_user_returns_empty_list_when_no_todos(self, todo_manager):
        """Test that get_todos_by_user returns empty list when user has no todos."""
        todos = todo_manager.get_todos_by_user("nonexistent_user")
        assert todos == []
        assert isinstance(todos, list)

    def test_get_todos_by_user_returns_single_todo(self, todo_manager):
        """Test retrieving a single todo for a user."""
        # Create a todo for testuser
        todo_manager.create_todo(
            title="My First Todo",
            details="This is my first todo",
            priority=Priority.HIGH,
            owner="testuser"
        )

        todos = todo_manager.get_todos_by_user("testuser")
        assert len(todos) == 1
        assert todos[0].title == "My First Todo"
        assert todos[0].owner == "testuser"

    def test_get_todos_by_user_returns_multiple_todos(self, todo_manager):
        """Test retrieving multiple todos for a user."""
        # Create multiple todos for testuser
        todo_manager.create_todo("Todo 1", "Details 1", Priority.HIGH, "testuser")
        todo_manager.create_todo("Todo 2", "Details 2", Priority.MID, "testuser")
        todo_manager.create_todo("Todo 3", "Details 3", Priority.LOW, "testuser")

        todos = todo_manager.get_todos_by_user("testuser")
        assert len(todos) == 3
        assert all(todo.owner == "testuser" for todo in todos)

    def test_get_todos_by_user_filters_by_owner(self, todo_manager):
        """Test that get_todos_by_user correctly filters todos by owner."""
        # Create todos for different users
        todo_manager.create_todo("User1 Todo1", "Details", Priority.HIGH, "user1")
        todo_manager.create_todo("User1 Todo2", "Details", Priority.MID, "user1")
        todo_manager.create_todo("User2 Todo1", "Details", Priority.LOW, "user2")
        todo_manager.create_todo("User3 Todo1", "Details", Priority.HIGH, "user3")

        # Verify filtering for each user
        user1_todos = todo_manager.get_todos_by_user("user1")
        assert len(user1_todos) == 2
        assert all(todo.owner == "user1" for todo in user1_todos)

        user2_todos = todo_manager.get_todos_by_user("user2")
        assert len(user2_todos) == 1
        assert user2_todos[0].owner == "user2"

        user3_todos = todo_manager.get_todos_by_user("user3")
        assert len(user3_todos) == 1
        assert user3_todos[0].owner == "user3"

    def test_get_todos_by_user_returns_todos_with_correct_status(self, todo_manager):
        """Test that returned todos have correct status information."""
        # Create todos with different statuses
        todo1 = todo_manager.create_todo("Pending Todo", "Details", Priority.HIGH, "testuser")
        assert todo1.status == Status.PENDING

        todo_manager.update_todo(todo1.id, status=Status.COMPLETED)
        todo2 = todo_manager.create_todo("Another Todo", "Details", Priority.MID, "testuser")

        todos = todo_manager.get_todos_by_user("testuser")
        assert len(todos) == 2
        # Check that todos maintain their status
        pending_count = sum(1 for todo in todos if todo.status == Status.PENDING)
        completed_count = sum(1 for todo in todos if todo.status == Status.COMPLETED)
        assert pending_count == 1
        assert completed_count == 1

    def test_get_todos_preserves_all_fields(self, todo_manager):
        """Test that all todo fields are preserved when retrieved."""
        title = "Complete Todo"
        details = "Full details here"
        priority = Priority.HIGH
        owner = "testuser"

        created_todo = todo_manager.create_todo(
            title=title,
            details=details,
            priority=priority,
            owner=owner
        )

        retrieved_todos = todo_manager.get_todos_by_user(owner)
        retrieved_todo = retrieved_todos[0]

        assert retrieved_todo.id == created_todo.id
        assert retrieved_todo.title == title
        assert retrieved_todo.details == details
        assert retrieved_todo.priority == priority
        assert retrieved_todo.owner == owner
        assert retrieved_todo.status == Status.PENDING
        assert retrieved_todo.created_at == created_todo.created_at


class TestTask5ViewTodoDetails:
    """Test cases for Task 5: View to-do-list item details."""

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

    def test_get_todo_by_id_returns_correct_todo(self, todo_manager):
        """Test retrieving a specific todo by ID."""
        todo = todo_manager.create_todo(
            title="Specific Todo",
            details="Find me by ID",
            priority=Priority.HIGH,
            owner="testuser"
        )

        retrieved = todo_manager.get_todo_by_id(todo.id)
        assert retrieved is not None
        assert retrieved.id == todo.id
        assert retrieved.title == "Specific Todo"

    def test_get_todo_by_id_returns_none_for_nonexistent_id(self, todo_manager):
        """Test that get_todo_by_id returns None for nonexistent ID."""
        result = todo_manager.get_todo_by_id("nonexistent-id-12345")
        assert result is None

    def test_todo_details_contain_all_required_fields(self, todo_manager):
        """Test that todo details contain all required fields."""
        todo = todo_manager.create_todo(
            title="Complete Details",
            details="Full description here",
            priority=Priority.MID,
            owner="testuser"
        )

        retrieved = todo_manager.get_todo_by_id(todo.id)

        # Verify all required fields are present
        assert hasattr(retrieved, 'id')
        assert hasattr(retrieved, 'title')
        assert hasattr(retrieved, 'details')
        assert hasattr(retrieved, 'priority')
        assert hasattr(retrieved, 'status')
        assert hasattr(retrieved, 'owner')
        assert hasattr(retrieved, 'created_at')
        assert hasattr(retrieved, 'updated_at')

    def test_todo_details_show_correct_priority(self, todo_manager):
        """Test that todo details display correct priority levels."""
        priorities = [Priority.HIGH, Priority.MID, Priority.LOW]

        for priority in priorities:
            todo = todo_manager.create_todo(
                title=f"Priority {priority.value}",
                details="Details",
                priority=priority,
                owner="testuser"
            )

            retrieved = todo_manager.get_todo_by_id(todo.id)
            assert retrieved.priority == priority
            assert retrieved.priority.value in ["HIGH", "MID", "LOW"]

    def test_todo_details_show_correct_status(self, todo_manager):
        """Test that todo details display correct status."""
        # Create pending todo
        pending_todo = todo_manager.create_todo(
            title="Pending",
            details="Details",
            priority=Priority.HIGH,
            owner="testuser"
        )

        retrieved_pending = todo_manager.get_todo_by_id(pending_todo.id)
        assert retrieved_pending.status == Status.PENDING

        # Mark as completed
        todo_manager.update_todo(pending_todo.id, status=Status.COMPLETED)
        retrieved_completed = todo_manager.get_todo_by_id(pending_todo.id)
        assert retrieved_completed.status == Status.COMPLETED

    def test_todo_details_show_owner_information(self, todo_manager):
        """Test that todo details include owner information."""
        owner = "specific_user"
        todo = todo_manager.create_todo(
            title="Owned Todo",
            details="Details",
            priority=Priority.HIGH,
            owner=owner
        )

        retrieved = todo_manager.get_todo_by_id(todo.id)
        assert retrieved.owner == owner

    def test_todo_details_show_timestamps(self, todo_manager):
        """Test that todo details include created and updated timestamps."""
        todo = todo_manager.create_todo(
            title="Timestamped Todo",
            details="Details",
            priority=Priority.HIGH,
            owner="testuser"
        )

        retrieved = todo_manager.get_todo_by_id(todo.id)
        assert retrieved.created_at is not None
        assert retrieved.updated_at is not None
        # Both should be ISO format strings
        assert "T" in retrieved.created_at
        assert "T" in retrieved.updated_at

    def test_todo_details_updated_at_changes_on_update(self, todo_manager):
        """Test that updated_at timestamp changes when todo is modified."""
        import time

        todo = todo_manager.create_todo(
            title="Original Title",
            details="Details",
            priority=Priority.HIGH,
            owner="testuser"
        )

        original_updated_at = todo.updated_at
        created_at = todo.created_at

        # Wait a moment to ensure timestamp difference
        time.sleep(0.01)

        # Update the todo
        todo_manager.update_todo(todo.id, title="Updated Title")
        updated_todo = todo_manager.get_todo_by_id(todo.id)

        assert updated_todo.created_at == created_at
        assert updated_todo.updated_at != original_updated_at


class TestTask6MarkTodoCompleted:
    """Test cases for Task 6: Mark a to-do-list item as completed."""

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

    def test_mark_pending_todo_as_completed(self, todo_manager):
        """Test marking a pending todo as completed."""
        todo = todo_manager.create_todo(
            title="Pending Todo",
            details="To be completed",
            priority=Priority.HIGH,
            owner="testuser"
        )

        assert todo.status == Status.PENDING

        # Mark as completed
        updated = todo_manager.update_todo(todo.id, status=Status.COMPLETED)

        assert updated is not None
        assert updated.status == Status.COMPLETED

    def test_mark_completed_todo_remains_completed(self, todo_manager):
        """Test that marking an already completed todo keeps it completed."""
        todo = todo_manager.create_todo(
            title="Todo",
            details="Details",
            priority=Priority.HIGH,
            owner="testuser"
        )

        # Mark as completed
        todo_manager.update_todo(todo.id, status=Status.COMPLETED)
        retrieved = todo_manager.get_todo_by_id(todo.id)
        assert retrieved.status == Status.COMPLETED

        # Mark as completed again (should not fail)
        updated = todo_manager.update_todo(todo.id, status=Status.COMPLETED)
        assert updated.status == Status.COMPLETED

    def test_mark_only_specific_todo_completed(self, todo_manager):
        """Test that only the selected todo is marked as completed."""
        todo1 = todo_manager.create_todo("Todo 1", "Details", Priority.HIGH, "testuser")
        todo2 = todo_manager.create_todo("Todo 2", "Details", Priority.MID, "testuser")
        todo3 = todo_manager.create_todo("Todo 3", "Details", Priority.LOW, "testuser")

        # Mark only todo2 as completed
        todo_manager.update_todo(todo2.id, status=Status.COMPLETED)

        # Verify correct todos are completed
        retrieved1 = todo_manager.get_todo_by_id(todo1.id)
        retrieved2 = todo_manager.get_todo_by_id(todo2.id)
        retrieved3 = todo_manager.get_todo_by_id(todo3.id)

        assert retrieved1.status == Status.PENDING
        assert retrieved2.status == Status.COMPLETED
        assert retrieved3.status == Status.PENDING

    def test_mark_completed_persists_to_storage(self, todo_manager):
        """Test that marking a todo as completed persists to storage."""
        todo = todo_manager.create_todo(
            title="Persistent Todo",
            details="Details",
            priority=Priority.HIGH,
            owner="testuser"
        )

        # Mark as completed
        todo_manager.update_todo(todo.id, status=Status.COMPLETED)

        # Create new manager instance (simulates fresh load)
        todo_manager2 = TodoManager(todo_manager.todos_file)
        retrieved = todo_manager2.get_todo_by_id(todo.id)

        assert retrieved is not None
        assert retrieved.status == Status.COMPLETED

    def test_mark_completed_prevents_duplicate_completion(self, todo_manager):
        """Test that duplicate completion attempts don't cause errors."""
        todo = todo_manager.create_todo(
            title="Todo",
            details="Details",
            priority=Priority.HIGH,
            owner="testuser"
        )

        # First completion
        todo_manager.update_todo(todo.id, status=Status.COMPLETED)
        retrieved1 = todo_manager.get_todo_by_id(todo.id)
        assert retrieved1.status == Status.COMPLETED

        # Second completion attempt should not fail
        todo_manager.update_todo(todo.id, status=Status.COMPLETED)
        retrieved2 = todo_manager.get_todo_by_id(todo.id)
        assert retrieved2.status == Status.COMPLETED

    def test_mark_completed_updates_updated_at_timestamp(self, todo_manager):
        """Test that marking as completed updates the updated_at timestamp."""
        import time

        todo = todo_manager.create_todo(
            title="Todo",
            details="Details",
            priority=Priority.HIGH,
            owner="testuser"
        )

        original_updated_at = todo.updated_at

        # Wait a moment to ensure timestamp difference
        time.sleep(0.01)

        # Mark as completed
        todo_manager.update_todo(todo.id, status=Status.COMPLETED)
        updated_todo = todo_manager.get_todo_by_id(todo.id)

        assert updated_todo.updated_at != original_updated_at

    def test_mark_completed_by_id_with_multiple_users(self, todo_manager):
        """Test marking a todo as completed for a specific user."""
        # Create todos for different users
        user1_todo = todo_manager.create_todo("User1 Todo", "Details", Priority.HIGH, "user1")
        user2_todo = todo_manager.create_todo("User2 Todo", "Details", Priority.HIGH, "user2")

        # Mark user1's todo as completed
        todo_manager.update_todo(user1_todo.id, status=Status.COMPLETED)

        # Verify only user1's todo is marked as completed
        retrieved_user1 = todo_manager.get_todo_by_id(user1_todo.id)
        retrieved_user2 = todo_manager.get_todo_by_id(user2_todo.id)

        assert retrieved_user1.status == Status.COMPLETED
        assert retrieved_user2.status == Status.PENDING

    def test_mark_nonexistent_todo_returns_none(self, todo_manager):
        """Test that marking a nonexistent todo returns None."""
        result = todo_manager.update_todo("nonexistent-id", status=Status.COMPLETED)
        assert result is None

    def test_completion_status_values_are_correct(self, todo_manager):
        """Test that completion uses correct Status enum values."""
        todo = todo_manager.create_todo(
            title="Todo",
            details="Details",
            priority=Priority.HIGH,
            owner="testuser"
        )

        # Mark as completed
        updated = todo_manager.update_todo(todo.id, status=Status.COMPLETED)

        # Verify status value is correct
        assert updated.status == Status.COMPLETED
        assert updated.status.value == "COMPLETED"
        assert isinstance(updated.status, Status)
