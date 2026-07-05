"""Failing auth tests for the AMO benchmark example (not collected by AMO's own suite)."""

from app.auth import authenticate


def test_rejects_unknown_user():
    assert authenticate("mallory", "guess") is False


def test_accepts_known_user():
    assert authenticate("ada", "correct-horse") is True
