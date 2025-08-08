"""Test utilities for the SpectralAPI tests.

This module contains reusable test components including signal
generators and test data structures for spectrum analysis testing. It
provides tools for creating synthetic signals with known frequency
components for validating the spectrum analysis functionality.
"""

import numpy as np

from src.spectrum_api.models.input_models import DataArray, FrequencyBin


def generate_real_signal(
    frequency_bins: list[FrequencyBin], fs: float, duration: float
) -> DataArray:
    """Test signal generator.

    Generate a sum of cosine waves with specified frequencies, amplitudes, and phases.
    This function creates a synthetic signal by summing multiple
    cosine waves, each defined by a FrequencyBin object. The signal is
    generated using vectorized numpy operations for efficiency.
    The function validates that the frequency_bins list is not empty and
    generates a time-domain signal that can be used for testing spectrum
    analysis.

    Args:
        frequency_bins: List of FrequencyBin defining the frequency components
        fs: Sampling frequency in Hz
        duration: Duration of the signal in seconds

    Returns:
        Numpy array containing the generated signal

    Raises:
        ValueError: If the frequency_bins list is empty
    """
    if not frequency_bins:
        raise ValueError("frequency_bins must be a non-empty list")

    t = np.arange(0, duration, 1 / fs)
    freqs = np.array([fb.frequency for fb in frequency_bins])
    amps = np.array([fb.module for fb in frequency_bins])
    phases = np.array([fb.phase for fb in frequency_bins])

    # Compute angular frequencies once
    angular_freqs = 2 * np.pi * freqs[:, None] * t

    # Vectorized cosine waves generation and summation
    signal = np.dot(amps, np.cos(angular_freqs + phases[:, None]))

    return signal.tolist()
