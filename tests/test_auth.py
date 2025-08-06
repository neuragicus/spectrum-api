"""Tests for the authentication module."""

import pytest
from fastapi.testclient import TestClient

from spectrum_api.config.auth import API_KEY_HEADER_NAME
from src.spectrum_api.models.input_models import SpectrumAnalysisRequest

TEST_API_KEY = "TEST_API_KEY"


@pytest.mark.parametrize(
    "header_name, used_token, expected_return_status",
    [
        (API_KEY_HEADER_NAME, TEST_API_KEY, 200),
        (API_KEY_HEADER_NAME, "XXXX", 403),
        ("WRONG_API_KEY_NAME", TEST_API_KEY, 403),
    ],
)
def test_api_authentication(
    test_client: TestClient,
    header_name: str,
    used_token: str,
    expected_return_status: int,
) -> None:
    """Test API key authentication with various header configurations."""
    request_data = SpectrumAnalysisRequest(
        time_interval=1,
        data=[1, 2, 3, 4, 5],
    )

    response = test_client.post(
        "/analyze_spectrum",
        content=request_data.model_dump_json(),
        headers={header_name: used_token},
    )

    assert response.status_code == expected_return_status
