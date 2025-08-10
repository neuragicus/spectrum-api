"""Authentication module for the Spectrum API.

This module provides API key-based authentication using FastAPI's
security features. It validates API keys from request headers against
environment-configured values.
"""

import os
from http import HTTPStatus
from typing import Any

from fastapi import Depends, HTTPException, Security
from fastapi.security import APIKeyHeader

# Environment variable names for API key configuration
API_KEY_HEADER_NAME: str = os.environ.get("API_KEY_NAME", "X-API-Key")
API_KEY_VALUE: str = os.environ.get("API_KEY_VALUE", "")

# FastAPI security header for API key authentication
api_key_header = APIKeyHeader(name=API_KEY_HEADER_NAME)


def validate_api_key(api_key: str = Security(api_key_header)) -> None:
    """Validate the provided API key against the configured environment value.

    Args:
        api_key: The API key from the request header

    Raises:
        HTTPException: If the API key is invalid or missing
    """

    if not api_key or api_key != API_KEY_VALUE:
        raise HTTPException(
            status_code=HTTPStatus.FORBIDDEN.value, detail="Invalid or missing API key"
        )


def get_authentication_dependencies() -> list[Any]:
    """Get authentication dependencies for FastAPI endpoints.

    This function returns a list of dependencies that can be used to protect
    API endpoints with API key authentication.

    Returns:
        List of FastAPI dependencies for authentication

    Raises:
        ValueError: If the API key environment variable is not configured

    """
    if not API_KEY_VALUE:
        raise ValueError(
            "API_KEY_VALUE environment variable is not configured. "
            "Please set this variable to enable API key authentication."
        )

    return [Depends(validate_api_key)]
