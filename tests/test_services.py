"""Tests for the spectrum analysis service.

This module contains comprehensive tests for the spectrum analysis
functionality, validating that the FFT correctly identifies frequency
components, amplitudes, and phases from synthetic signals with known
properties.
"""

import math

import numpy as np
import pytest

from spectrum_api.constants import (
    FREQUENCY_MODULE_TOLERANCE,
    FREQUENCY_PHASE_TOLERANCE,
    FREQUENCY_TOLERANCE,
)
from src.spectrum_api.models.input_models import FrequencyBin
from src.spectrum_api.services.fft import SpectrumAnalyzer
from tests.utils import generate_real_signal


class ApproximateFrequencyBin(FrequencyBin):
    """FrequencyBin with overload approximate equality comparison for tests only.

    Args:
        frequency: The frequency value
        module: The magnitude/module value
        phase: The phase value
    """

    def __eq__(self, other: object) -> bool:
        """Compare FrequencyBin objects with tolerance for floating point."""
        if not isinstance(other, FrequencyBin):
            return NotImplemented
        return (
            math.isclose(self.frequency, other.frequency, abs_tol=FREQUENCY_TOLERANCE)
            and math.isclose(
                self.module, other.module, abs_tol=FREQUENCY_MODULE_TOLERANCE
            )
            and math.isclose(self.phase, other.phase, abs_tol=FREQUENCY_PHASE_TOLERANCE)
        )


@pytest.mark.parametrize(
    "frequency_bins, expected_bins",
    [
        (
            [FrequencyBin(frequency=10.0, module=1.0, phase=0.0)],
            [ApproximateFrequencyBin(frequency=10.0, module=1.0, phase=0.0)],
        ),
        (
            [FrequencyBin(frequency=25.0, module=2.0, phase=np.pi / 4)],
            [ApproximateFrequencyBin(frequency=25.0, module=2.0, phase=np.pi / 4)],
        ),
        (
            [FrequencyBin(frequency=50.0, module=0.5, phase=-np.pi / 2)],
            [ApproximateFrequencyBin(frequency=50.0, module=0.5, phase=-np.pi / 2)],
        ),
        (
            [
                FrequencyBin(frequency=10.0, module=1.0, phase=0.0),
                FrequencyBin(frequency=20.0, module=0.5, phase=np.pi / 6),
            ],
            [
                ApproximateFrequencyBin(frequency=10.0, module=1.0, phase=0.0),
                ApproximateFrequencyBin(frequency=20.0, module=0.5, phase=np.pi / 6),
            ],
        ),
        (
            [
                FrequencyBin(frequency=15.0, module=2.0, phase=0.0),
                FrequencyBin(frequency=30.0, module=1.0, phase=np.pi / 3),
                FrequencyBin(frequency=45.0, module=0.3, phase=-np.pi / 4),
            ],
            [
                ApproximateFrequencyBin(frequency=15.0, module=2.0, phase=0.0),
                ApproximateFrequencyBin(frequency=30.0, module=1.0, phase=np.pi / 3),
                ApproximateFrequencyBin(frequency=45.0, module=0.3, phase=-np.pi / 4),
            ],
        ),
        (
            [FrequencyBin(frequency=1.0, module=0.1, phase=np.pi)],
            [ApproximateFrequencyBin(frequency=1.0, module=0.1, phase=np.pi)],
        ),
        (
            [FrequencyBin(frequency=100.0, module=5.0, phase=-np.pi)],
            [ApproximateFrequencyBin(frequency=100.0, module=5.0, phase=-np.pi)],
        ),
    ],
    ids=[
        "single_frequency_basic_sine",
        "single_frequency_phase_shifted",
        "single_frequency_cosine_equivalent",
        "two_frequencies_different_components",
        "three_frequencies_varying_amplitudes",
        "edge_case_low_frequency_small_amplitude",
        "edge_case_high_frequency_large_amplitude",
    ],
)
def test_spectrum_analysis_with_frequency_components(
    frequency_bins: list[FrequencyBin], expected_bins: list[FrequencyBin]
) -> None:
    """Test spectrum analysis with various frequency component combinations.

    This test validates that the FFT correctly identifies frequencies,
    amplitudes, and phases from signals composed of multiple frequency components.

    The test generates synthetic signals with known frequency characteristics
    and verifies that the spectrum analyzer can accurately recover these
    components within the defined tolerance limits.

    Args:
        frequency_bins: Input frequency components to generate the test signal
        expected_bins: Expected frequency components after spectrum analysis

    """
    fs = 1000  # Sampling frequency in Hz
    duration = 1.0  # Signal duration in seconds

    spectrum_analyzer = SpectrumAnalyzer()

    # Generate synthetic signal with known frequency components
    signal = generate_real_signal(frequency_bins, fs, duration)

    # Perform spectrum analysis
    spectrum_result = spectrum_analyzer.get_signal_spectrum(
        signal, time_interval=1 / fs
    )

    # Filter out noise (components with zero magnitude)
    actual_bins = [f for f in spectrum_result if f.module > 0]

    # Verify that analyzed components match expected components
    assert actual_bins == expected_bins


@pytest.mark.parametrize(
    "signals, expected_count",
    [([np.array([1.0, 2.0, 3.0, 4.0]), np.array([1.0, 2.0, 3.0, 4.0, 5.0])], 2)],
)
def test_spectrum_analyzer_cache_management(
    signals: list[np.ndarray], expected_count: int
) -> None:
    """Test the cache management of the spectrum analyzer."""
    analyzer = SpectrumAnalyzer()

    # Initial empty state
    assert analyzer.get_cache_info()["cached_signal_lengths"] == 0

    # Populate cache
    for signal in signals:
        analyzer.get_signal_spectrum(signal, 0.1)

    # Verify cache population
    cache_info = analyzer.get_cache_info()
    assert cache_info["cached_signal_lengths"] == expected_count

    # Clear and verify reset
    analyzer.clear_cache()
    assert analyzer.get_cache_info()["cached_signal_lengths"] == 0


def test_spectrum_analyzer_input_validation() -> None:
    """Test input validation for the spectrum analyzer.

    This test verifies that the analyzer properly validates input
    parameters and raises appropriate exceptions for invalid inputs.
    """
    analyzer = SpectrumAnalyzer()

    # Test empty signal
    with pytest.raises(ValueError, match="Input signal cannot be empty"):
        analyzer.get_signal_spectrum(np.array([]), 0.1)

    # Test zero sample spacing
    with pytest.raises(ValueError, match="Sample spacing must be positive"):
        analyzer.get_signal_spectrum(np.array([1.0, 2.0, 3.0]), 0.0)

    # Test negative sample spacing
    with pytest.raises(ValueError, match="Sample spacing must be positive"):
        analyzer.get_signal_spectrum(np.array([1.0, 2.0, 3.0]), -0.1)
