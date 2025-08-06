"""Constants for the SpectralAPI.

This module defines application-wide constants including spectrum_api metadata,
environment variable names, and field identifiers used throughout the
application.
"""

from .config.app_metadata import get_app_metadata

# App metadata
APP_METADATA = get_app_metadata()

# FFT Settings
FREQUENCY_TOLERANCE = 0.01
FREQUENCY_MODULE_TOLERANCE = 1e-4
FREQUENCY_PHASE_TOLERANCE = 1e-2

# Cache Settings
MAX_CACHE_ENTRIES = 200  # For FFT speed optimization
