"""Spectrum analysis service module.

This module provides functionality to analyze signal data using FFT and
return frequency domain results with magnitude and phase information.
"""

import numpy as np
import pyfftw

from ..constants import MAX_CACHE_ENTRIES
from ..models.input_models import DataArray, FrequencyBin


class SpectrumAnalyzer:
    """A class that performs fast FFT analysis with caching of FFTW plans and buffers.

    This analyzer is optimized for real-valued input signals and caches
    FFT plans and aligned buffers for signals of the same length to
    improve performance on repeated operations.
    """

    def __init__(self) -> None:
        """Initialize with an empty cache for FFT plans and buffers."""
        # Cache FFTW plans and buffers by signal length
        # cache typehint {signal_length: (fft_plan, input_buffer, output_buffer)}
        self._cache: dict[int, tuple[pyfftw.FFTW, np.ndarray, np.ndarray]] = {}

    def get_signal_spectrum(
        self, signal: DataArray | np.ndarray, time_interval: float
    ) -> list[FrequencyBin]:
        """Analyze the frequency spectrum of the input signal using FFT.

        This method computes the FFT spectrum of a real-valued time-domain signal
        and returns the frequency components with their corresponding magnitudes
        and phases.
        The method uses caching to optimize performance for signals of the same length.
        The magnitude scaling follows the convention where:
        - DC component (frequency 0) is scaled by 1/n
        - Other components are scaled by 2/n to account for negative frequencies
        - Nyquist frequency (for even-length signals) is scaled by 1/n

        Args:
            signal: 1D numpy array of real-valued time-domain samples
            time_interval: Time interval between samples in seconds

        Returns:
            List of FrequencyBin objects containing frequency, magnitude,
            and phase information for each frequency component in the spectrum

        Raises:
            ValueError: If signal is empty or sample_spacing is non-positive

        """

        n = len(signal)

        if n == 0:
            raise ValueError("Input signal cannot be empty")
        if time_interval <= 0:
            raise ValueError("Sample spacing must be positive")

        # Get or create cached FFT plan and buffers
        if n not in self._cache:
            self._create_fft_cache(n)

        fft_plan, input_buffer, output_buffer = self._cache[n]

        # Copy signal into aligned input buffer for optimal performance
        input_buffer[:] = signal

        # Perform FFT using cached plan
        fft_result = fft_plan(input_buffer, output_buffer)

        # Calculate frequency bins
        frequencies = np.fft.rfftfreq(n, time_interval)

        # Calculate properly scaled magnitudes
        magnitudes = self._calculate_scaled_magnitudes(fft_result, n)

        # Calculate phases
        phases = np.angle(fft_result)

        return [
            FrequencyBin(frequency=freq, module=mag, phase=phase)
            for freq, mag, phase in zip(frequencies, magnitudes, phases, strict=False)
        ]

    def _create_fft_cache(self, signal_length: int) -> None:
        """Create cache FFT plan and aligned buffers for the given signal length.

        Args:
            signal_length: Length of the signal for which to create the cache

        """
        # Clear cache if it's getting too big
        if len(self._cache) >= MAX_CACHE_ENTRIES:
            self.clear_cache()

        # Create aligned buffers for optimal FFTW performance
        input_buffer = pyfftw.empty_aligned(signal_length, dtype="float64")
        output_buffer = pyfftw.empty_aligned(signal_length // 2 + 1, dtype="complex128")

        # Create FFT plan with input buffer overwriting for memory efficiency
        fft_plan = pyfftw.builders.rfft(input_buffer, overwrite_input=True)

        self._cache[signal_length] = (fft_plan, input_buffer, output_buffer)

    @staticmethod
    def _calculate_scaled_magnitudes(
        fft_result: np.ndarray, signal_length: int
    ) -> np.ndarray:
        """Calculate properly scaled magnitudes from FFT result.

        For real FFT, the scaling accounts for the fact that positive and negative
        frequencies are combined, except for DC and Nyquist components.

        Args:
            fft_result: Complex FFT result array
            signal_length: Original signal length

        Returns:
            Array of scaled magnitudes

        """
        magnitudes = np.abs(fft_result) * 2 / signal_length

        # DC component should not be doubled
        magnitudes[0] /= 2

        # For even-length signals, Nyquist frequency should not be doubled
        if signal_length % 2 == 0:
            magnitudes[-1] /= 2

        return magnitudes

    def clear_cache(self) -> None:
        """Clear the internal cache of FFT plans and buffers to free memory."""
        self._cache.clear()

    def get_cache_info(self) -> dict[str, int | list[int]]:
        """Get information about the current cache state.

        Returns:
            Dictionary containing cache statistics including the number of cached
            signal lengths and total memory usage estimate

        """
        return {
            "cached_signal_lengths": len(self._cache),
            "signal_lengths": list(self._cache.keys()),
        }
