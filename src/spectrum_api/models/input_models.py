"""Input models for the SpectralAPI.

This module defines the Pydantic models used for spectrum analysis requests
and responses, including validation logic for input data.
"""

from typing import TypeAlias

from pydantic import BaseModel, Field, model_validator

from ..constants import FREQUENCY_MODULE_TOLERANCE, FREQUENCY_PHASE_TOLERANCE

# Custom type for the data array
DataArray: TypeAlias = list[float]


class SpectrumAnalysisRequest(BaseModel):
    """Request model for spectrum analysis.

    This model represents a request to analyze the frequency spectrum of a signal.
    It contains the time interval between data points and the signal data itself.

    :param time_interval: Time interval in seconds between consecutive data points
    :param data: Array of signal data points
    """

    time_interval: float | int = Field(
        ...,
        gt=0,
        description="Time interval (seconds) between consecutive data points.",
    )
    data: DataArray

    @model_validator(mode="after")
    def validate_data(self) -> "SpectrumAnalysisRequest":
        """Validate that the data field contains valid numeric values.

        This validator ensures that:
        - The data field is present and is a list
        - The list is not empty
        - All elements in the list are numeric (int or float)

        :return: The validated instance
        :raises ValueError: If the data validation fails
        """
        if not self.data or not isinstance(self.data, list):
            raise ValueError("Input data must be a non-empty list.")
        if not all(isinstance(x, int | float) for x in self.data):
            raise ValueError("All data points must be numeric.")
        return self


class FrequencyBin(BaseModel):
    """Model for a single frequency component in the spectrum."""

    frequency: float = Field(..., description="Frequency in Hz")
    module: float = Field(..., description="Magnitude of the frequency component")
    phase: float = Field(..., description="Phase in radians")

    @model_validator(mode="after")
    def zero_near_values(self) -> "FrequencyBin":
        """Set near-zero values to zero, according to tolerance."""
        if abs(self.module) < FREQUENCY_MODULE_TOLERANCE:
            self.module = 0.0
        if abs(self.phase) < FREQUENCY_PHASE_TOLERANCE:
            self.phase = 0.0
        return self


class SpectrumAnalysisResponse(BaseModel):
    """Response model for spectrum analysis results.

    This model contains the complete spectrum analysis results,
    including all frequency components found in the signal.

    :param result: List of spectrum analysis results for each frequency component
    """

    result: list[FrequencyBin] = Field(
        ..., description="List of spectrum analysis results"
    )
