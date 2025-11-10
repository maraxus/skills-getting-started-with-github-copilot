"""
Pytest configuration and shared fixtures for the test suite
"""

import pytest
from fastapi.testclient import TestClient
from src.app import app