"""Main entry point for the CLI To-Do List Application."""

import json
import os
from pathlib import Path


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
            # TODO: Show main app menu for logged-in user
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
    
    def run(self):
        """Start the application."""
        self.show_pre_login_menu()


def main():
    """Entry point of the application."""
    app = App()
    app.run()


if __name__ == "__main__":
    main()
