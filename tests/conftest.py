"""
Pytest configuration and shared fixtures for the test suite
"""

import pytest
from fastapi.testclient import TestClient
from src.app import app


@pytest.fixture(scope="session")
def test_client():
    """
    Create a test client that can be shared across test sessions
    """
    return TestClient(app)