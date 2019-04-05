from cli.load_users import load_users
import os


def test_load_users():
    """Test load users."""
    file_path = full_path("fixtures/valid_users.txt")
    load_users(file_path, "b", "c")


def full_path(path):
    """Return a full path."""
    return os.path.join(os.path.dirname(__file__), path)
