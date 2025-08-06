"""Main application entry point for the Spectral API.

This module sets up the FastAPI application with spectrum analysis
endpoints and authentication middleware. It provides the main API
interface for performing frequency domain analysis on signal data.
"""

import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.responses import ORJSONResponse

from src.spectrum_api.config.auth import get_authentication_dependencies
from src.spectrum_api.constants import APP_METADATA
from src.spectrum_api.endpoints.fft_real import fft_real
from src.spectrum_api.models.input_models import (
    SpectrumAnalysisRequest,
    SpectrumAnalysisResponse,
)
from src.spectrum_api.services.fft import SpectrumAnalyzer

APP_NAME = APP_METADATA.name
APP_VERSION = APP_METADATA.version

logger = logging.getLogger(APP_NAME)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, Any]:
    # Startup application
    logger.info(f"Starting {APP_NAME} v.{APP_VERSION}.")

    # Attach an instance of SpectrumAnalyzer to optimize future call using its cache
    app.state.spectrum_analyzer = SpectrumAnalyzer()
    yield
    logger.info(f"Shutting down {APP_NAME} v.{APP_VERSION} and clearing cache.")
    app.state.spectrum_analyzer.clear_cache()


# Create FastAPI application instance
app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    description="Perform signal spectrum analysis",
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
)


@app.post(
    "/analyze_spectrum",
    response_model=SpectrumAnalysisResponse,
    dependencies=get_authentication_dependencies(),
)
def analyze_spectrum_endpoint(
    request: SpectrumAnalysisRequest,
) -> SpectrumAnalysisResponse:
    """Analyze the spectrum of input signal data.

    This endpoint accepts signal data and performs frequency domain
    analysis using Fast Fourier Transform (FFT). The analysis returns
    the frequency components present in the signal along with their
    magnitudes and phases.

    The endpoint requires API key authentication and validates the input
    data before processing. Invalid data will result in a 400 Bad
    Request response.

    :param request: The spectrum analysis request containing time
        interval and signal data.
    :return: The spectrum analysis results with frequency components and
        their properties
    :raises HTTPException: If the request data is invalid or processing
        fails
    """
    try:
        return SpectrumAnalysisResponse(
            result=fft_real(
                spectrum_analyzer=app.state.spectrum_analyzer,
                signal=request.data,
                time_interval=request.time_interval,
            )
        )
    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e)) from e
