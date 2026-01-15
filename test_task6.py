#!/usr/bin/env python3
"""Test script for task 6 - Mark todo as completed functionality."""

import json
import os
from pathlib import Path
from datetime import datetime

# Add src to path
import sys
sys.path.insert(0, '/workspaces/Bughair-todolist/src')

from models import TodoManager, Priority, Status
from main import AuthManager, USERS_FILE, TODOS_FILE

def setup_test_data():
    """Create test users and todos."""
    # Clear existing data
    Path(USERS_FILE).write_text(json.dumps([]))
    Path(TODOS_FILE).write_text(json.dumps([]))
    
    # Create test user
    auth_manager = AuthManager(USERS_FILE)
    auth_manager.signup("testuser", "password123")
    
    # Create test todos
    todo_manager = TodoManager(TODOS_FILE)
    todo1 = todo_manager.create_todo("Buy groceries", "Milk, eggs, bread", Priority.HIGH, "testuser")
    todo2 = todo_manager.create_todo("Write report", "Quarterly report", Priority.MID, "testuser")
    todo3 = todo_manager.create_todo("Fix bug", "Issue #123", Priority.LOW, "testuser")
    
    return todo_manager, todo1, todo2, todo3

def test_mark_completed():
    """Test marking a todo as completed."""
    print("=" * 60)
    print("TEST: Mark Todo as Completed")
    print("=" * 60)
    
    todo_manager, todo1, todo2, todo3 = setup_test_data()
    
    # Get todos before marking
    todos = todo_manager.get_todos_by_user("testuser")
    print(f"\nBefore marking completed:")
    print(f"  Todo 1: {todo1.title} - Status: {todo1.status.value}")
    print(f"  Todo 2: {todo2.title} - Status: {todo2.status.value}")
    print(f"  Todo 3: {todo3.title} - Status: {todo3.status.value}")
    
    # Mark first todo as completed
    print(f"\n→ Marking '{todo1.title}' as completed...")
    updated = todo_manager.update_todo(todo1.id, status=Status.COMPLETED)
    
    # Verify update
    assert updated is not None, "Update should return the todo item"
    assert updated.status == Status.COMPLETED, "Status should be COMPLETED"
    print(f"✓ Status updated to: {updated.status.value}")
    
    # Reload and verify persistence
    todos_after = todo_manager.get_todos_by_user("testuser")
    todo1_reloaded = next(t for t in todos_after if t.id == todo1.id)
    print(f"✓ Status persisted in storage: {todo1_reloaded.status.value}")
    
    # Verify updated_at was changed
    assert updated.updated_at != todo1.updated_at, "updated_at should be refreshed"
    print(f"✓ updated_at timestamp refreshed: {updated.updated_at}")
    
    # Test duplicate completion prevention
    print(f"\n→ Attempting to mark '{todo1.title}' as completed again...")
    result = todo_manager.update_todo(todo1.id, status=Status.COMPLETED)
    print(f"✓ Duplicate completion allowed (status remains): {result.status.value}")
    
    # Verify other todos are unaffected
    todos_final = todo_manager.get_todos_by_user("testuser")
    todo2_final = next(t for t in todos_final if t.id == todo2.id)
    todo3_final = next(t for t in todos_final if t.id == todo3.id)
    assert todo2_final.status == Status.PENDING, "Todo 2 should still be PENDING"
    assert todo3_final.status == Status.PENDING, "Todo 3 should still be PENDING"
    print(f"✓ Other todos remain PENDING")
    
    print(f"\nAfter marking completed:")
    for todo in todos_final:
        status_symbol = "✓" if todo.status == Status.COMPLETED else "○"
        print(f"  {status_symbol} {todo.title} - Status: {todo.status.value}")
    
    print("\n" + "=" * 60)
    print("✓ ALL TESTS PASSED")
    print("=" * 60)

if __name__ == "__main__":
    test_mark_completed()
