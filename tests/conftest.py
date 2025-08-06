"""Fixture definitions for the SpectralAPI tests."""

from unittest.mock import MagicMock

import pytest
from starlette.testclient import TestClient

from src.spectrum_api.config import auth


@pytest.fixture
def test_client() -> TestClient:
    """Create a TestClient instance for testing the FastAPI application.

    :return: Configured TestClient instance for making test requests to
        the API
    """
    # Set test API key
    auth.API_KEY_VALUE = "TEST_API_KEY"

    # Import after the patch is applied
    from main import app

    # Mock the spectrum_api state with spectrum analyzer
    app.state = MagicMock()
    client = TestClient(app)

    return client
