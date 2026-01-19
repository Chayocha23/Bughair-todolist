"""Unit tests for Task 1: Sign up and log in functionality."""

import pytest
import tempfile
from pathlib import Path

# Add src to path for imports
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from main import AuthManager


class TestAuthManager:
    """Test cases for AuthManager class."""

    @pytest.fixture
    def temp_users_file(self):
        """Create a temporary users file for testing."""
        with tempfile.NamedTemporaryFile(mode='w+', suffix='.json', delete=False) as f:
            f.write('[]')
            temp_path = Path(f.name)
        yield temp_path
        # Cleanup
        temp_path.unlink(missing_ok=True)

    @pytest.fixture
    def auth_manager(self, temp_users_file):
        """Create AuthManager instance with temporary file."""
        return AuthManager(temp_users_file)

    def test_signup_success(self, auth_manager):
        """Test successful user signup."""
        result = auth_manager.signup("testuser", "password123")
        assert result is True

        # Verify user was saved
        users = auth_manager.load_users()
        assert len(users) == 1
        assert users[0]["username"] == "testuser"
        assert users[0]["password"] == "password123"

    def test_signup_duplicate_username(self, auth_manager):
        """Test signup fails when username already exists."""
        # First signup succeeds
        auth_manager.signup("testuser", "password123")

        # Second signup with same username fails
        result = auth_manager.signup("testuser", "different_password")
        assert result is False

    def test_login_success(self, auth_manager):
        """Test successful login."""
        # Create user first
        auth_manager.signup("testuser", "password123")

        # Login should succeed
        result = auth_manager.login("testuser", "password123")
        assert result is True

    def test_login_wrong_password(self, auth_manager):
        """Test login fails with wrong password."""
        # Create user
        auth_manager.signup("testuser", "password123")

        # Login with wrong password should fail
        result = auth_manager.login("testuser", "wrongpassword")
        assert result is False

    def test_login_nonexistent_user(self, auth_manager):
        """Test login fails for nonexistent user."""
        result = auth_manager.login("nonexistent", "password123")
        assert result is False