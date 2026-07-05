"""Toy auth module for the AMO benchmark example."""

USERS = {"ada": "correct-horse"}


def authenticate(username: str, password: str) -> bool:
    stored = USERS.get(username)
    # Example bug for the debug task: None-unsafe comparison.
    return stored == password
