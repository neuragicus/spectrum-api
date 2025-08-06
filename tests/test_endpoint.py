"""Tests for the main application endpoints."""

from typing import Any

import pytest

from spectrum_api.config.auth import API_KEY_HEADER_NAME
from tests.test_auth import TEST_API_KEY


@pytest.mark.parametrize(
    "payload,expected_status",
    [
        ({"time_interval": 5, "data": []}, 422),
        ({"time_interval": 5, "data": [1, "invalid", 3]}, 422),
        ({"time_interval": 0, "data": [1, 2, 3]}, 422),
        ({"time_interval": -1, "data": [1, 2, 3]}, 422),
        ({"data": [1, 2, 3]}, 422),
        ({"time_interval": 5}, 422),
        ({"time_interval": 5, "data": [0, 0.33, 8, 8, 8]}, 200),
    ],
    ids=[
        "empty_data_list",
        "invalid_data_type",
        "zero_time_interval",
        "negative_time_interval",
        "missing_time_interval",
        "missing_data",
        "valid_payload",
    ],
)
def test_api_response(test_client: Any, payload: dict, expected_status: int) -> None:
    """Test API endpoint responses for various payload configurations."""
    response = test_client.post(
        "/analyze_spectrum", headers={API_KEY_HEADER_NAME: TEST_API_KEY}, json=payload
    )
    assert response.status_code == expected_status
