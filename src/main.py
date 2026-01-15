"""Main entry point for the CLI To-Do List Application."""

import json
import os
from pathlib import Path
from models import TodoManager, Priority, Status


# Data file paths
DATA_DIR = Path("data")
USERS_FILE = DATA_DIR / "users.json"
TODOS_FILE = DATA_DIR / "todos.json"


def ensure_data_files():
    """Ensure data directory and files exist."""
    DATA_DIR.mkdir(exist_ok=True)
    
    if not USERS_FILE.exists():
        USERS_FILE.write_text(json.dumps([]))
    
    if not TODOS_FILE.exists():
        TODOS_FILE.write_text(json.dumps([]))


class AuthManager:
    """Manages user authentication and registration."""
    
    def __init__(self, users_file: Path = USERS_FILE):
        self.users_file = users_file
    
    def load_users(self) -> list:
        """Load users from JSON file."""
        with open(self.users_file, "r") as f:
            return json.load(f)
    
    def save_users(self, users: list):
        """Save users to JSON file."""
        with open(self.users_file, "w") as f:
            json.dump(users, f, indent=2)
    
    def user_exists(self, username: str) -> bool:
        """Check if a user exists."""
        users = self.load_users()
        return any(user["username"] == username for user in users)
    
    def login(self, username: str, password: str) -> bool:
        """Authenticate a user."""
        users = self.load_users()
        for user in users:
            if user["username"] == username and user["password"] == password:
                return True
        return False
    
    def signup(self, username: str, password: str) -> bool:
        """Register a new user."""
        if self.user_exists(username):
            return False
        
        users = self.load_users()
        users.append({"username": username, "password": password})
        self.save_users(users)
        return True


class App:
    """Main application class for the CLI."""
    
    def __init__(self):
        self.auth_manager = AuthManager()
        self.todo_manager = TodoManager(TODOS_FILE)
        self.current_user = None
        ensure_data_files()
    
    def show_pre_login_menu(self):
        """Display pre-login menu and handle user input."""
        while True:
            print("\n" + "="*40)
            print("Welcome to Todo List Application")
            print("="*40)
            print("[1] Login")
            print("[2] Sign Up")
            print("[3] Exit")
            print("="*40)
            
            choice = input("Enter your choice (1-3): ").strip()
            
            if choice == "1":
                self.handle_login()
            elif choice == "2":
                self.handle_signup()
            elif choice == "3":
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")
    
    def handle_login(self):
        """Handle user login."""
        username = input("Enter username: ").strip()
        password = input("Enter password: ").strip()
        
        if self.auth_manager.login(username, password):
            self.current_user = username
            print(f"\nWelcome back, {username}!")
            self.show_main_menu()
            return True
        else:
            print("Invalid username or password.")
            return False
    
    def handle_signup(self):
        """Handle user sign up."""
        username = input("Enter new username: ").strip()
        password = input("Enter password: ").strip()
        confirm_password = input("Confirm password: ").strip()
        
        if password != confirm_password:
            print("Passwords do not match.")
            return False
        
        if self.auth_manager.signup(username, password):
            print(f"Account created successfully for {username}!")
            return True
        else:
            print("Username already exists.")
            return False
    
    def show_main_menu(self):
        """Display main menu for logged-in user."""
        while self.current_user:
            print("\n" + "="*40)
            print(f"Welcome, {self.current_user}")
            print("="*40)
            print("[1] Create a new todo")
            print("[2] View my todos")
            print("[3] Edit a todo")
            print("[4] Mark todo as completed")
            print("[5] Delete a todo")
            print("[6] Logout")
            print("="*40)
            
            choice = input("Enter your choice (1-6): ").strip()
            
            if choice == "1":
                self.handle_create_todo()
            elif choice == "2":
                self.handle_view_todos()
            elif choice == "3":
                self.handle_edit_todo()
            elif choice == "4":
                self.handle_mark_completed()
            elif choice == "5":
                self.handle_delete_todo()
            elif choice == "6":
                print(f"Goodbye, {self.current_user}!")
                self.current_user = None
                break
            else:
                print("Invalid choice. Please try again.")
    
    def handle_create_todo(self):
        """Handle creating a new todo."""
        print("\n--- Create New Todo ---")
        title = input("Enter todo title: ").strip()
        if not title:
            print("Title cannot be empty.")
            return
        
        details = input("Enter todo details: ").strip()
        
        print("\nSelect priority:")
        print("[1] HIGH")
        print("[2] MID")
        print("[3] LOW")
        priority_choice = input("Enter priority (1-3): ").strip()
        
        priority_map = {"1": Priority.HIGH, "2": Priority.MID, "3": Priority.LOW}
        if priority_choice not in priority_map:
            print("Invalid priority choice.")
            return
        
        priority = priority_map[priority_choice]
        
        todo = self.todo_manager.create_todo(
            title=title,
            details=details,
            priority=priority,
            owner=self.current_user,
        )
        print(f"\nTodo created successfully! (ID: {todo.id})")
    
    def handle_view_todos(self):
        """Handle viewing user's todos."""
        todos = self.todo_manager.get_todos_by_user(self.current_user)
        
        if not todos:
            print("\nYou have no todos.")
            return
        
        print(f"\n--- Your Todos ({len(todos)}) ---")
        for i, todo in enumerate(todos, 1):
            status_symbol = "✓" if todo.status == Status.COMPLETED else "○"
            print(f"\n[{i}] {status_symbol} {todo.title}")
            print(f"    Details: {todo.details}")
            print(f"    Priority: {todo.priority.value}")
            print(f"    Status: {todo.status.value}")
            print(f"    ID: {todo.id}")
    
    def handle_edit_todo(self):
        """Handle editing a todo."""
        todos = self.todo_manager.get_todos_by_user(self.current_user)
        
        if not todos:
            print("\nYou have no todos to edit.")
            return
        
        print("\n--- Select Todo to Edit ---")
        for i, todo in enumerate(todos, 1):
            print(f"[{i}] {todo.title}")
        
        choice = input("Enter todo number to edit: ").strip()
        try:
            index = int(choice) - 1
            if 0 <= index < len(todos):
                todo = todos[index]
                self._edit_todo_fields(todo)
            else:
                print("Invalid choice.")
        except ValueError:
            print("Please enter a valid number.")
    
    def _edit_todo_fields(self, todo):
        """Edit individual fields of a todo."""
        print(f"\n--- Editing: {todo.title} ---")
        print("[1] Edit title")
        print("[2] Edit details")
        print("[3] Edit priority")
        print("[4] Cancel")
        
        choice = input("What would you like to edit? (1-4): ").strip()
        
        if choice == "1":
            new_title = input("Enter new title: ").strip()
            if new_title:
                self.todo_manager.update_todo(todo.id, title=new_title)
                print("Title updated successfully!")
            else:
                print("Title cannot be empty.")
        elif choice == "2":
            new_details = input("Enter new details: ").strip()
            self.todo_manager.update_todo(todo.id, details=new_details)
            print("Details updated successfully!")
        elif choice == "3":
            print("Select new priority:")
            print("[1] HIGH")
            print("[2] MID")
            print("[3] LOW")
            priority_choice = input("Enter priority (1-3): ").strip()
            priority_map = {"1": Priority.HIGH, "2": Priority.MID, "3": Priority.LOW}
            if priority_choice in priority_map:
                self.todo_manager.update_todo(
                    todo.id, priority=priority_map[priority_choice]
                )
                print("Priority updated successfully!")
            else:
                print("Invalid priority choice.")
        elif choice == "4":
            print("Edit cancelled.")
        else:
            print("Invalid choice.")
    
    def handle_mark_completed(self):
        """Handle marking a todo as completed."""
        todos = self.todo_manager.get_todos_by_user(self.current_user)
        
        if not todos:
            print("\nYou have no todos.")
            return
        
        print("\n--- Select Todo to Mark Completed ---")
        for i, todo in enumerate(todos, 1):
            status_symbol = "✓" if todo.status == Status.COMPLETED else "○"
            print(f"[{i}] {status_symbol} {todo.title}")
        
        choice = input("Enter todo number: ").strip()
        try:
            index = int(choice) - 1
            if 0 <= index < len(todos):
                todo = todos[index]
                if todo.status == Status.COMPLETED:
                    print("This todo is already completed.")
                else:
                    self.todo_manager.update_todo(todo.id, status=Status.COMPLETED)
                    print("Todo marked as completed!")
            else:
                print("Invalid choice.")
        except ValueError:
            print("Please enter a valid number.")
    
    def handle_delete_todo(self):
        """Handle deleting a todo."""
        todos = self.todo_manager.get_todos_by_user(self.current_user)
        
        if not todos:
            print("\nYou have no todos to delete.")
            return
        
        print("\n--- Select Todo to Delete ---")
        for i, todo in enumerate(todos, 1):
            print(f"[{i}] {todo.title}")
        
        choice = input("Enter todo number to delete: ").strip()
        try:
            index = int(choice) - 1
            if 0 <= index < len(todos):
                todo = todos[index]
                confirm = input(
                    f"Are you sure you want to delete '{todo.title}'? (y/n): "
                ).strip().lower()
                if confirm == "y":
                    if self.todo_manager.delete_todo(todo.id):
                        print("Todo deleted successfully!")
                    else:
                        print("Failed to delete todo.")
                else:
                    print("Deletion cancelled.")
            else:
                print("Invalid choice.")
        except ValueError:
            print("Please enter a valid number.")
    
    def run(self):
        """Start the application."""
        self.show_pre_login_menu()


def main():
    """Entry point of the application."""
    app = App()
    app.run()


if __name__ == "__main__":
    main()
