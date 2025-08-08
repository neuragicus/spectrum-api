""" """

from ..models.input_models import DataArray, FrequencyBin
from ..services.fft import SpectrumAnalyzer


def fft_real(
    spectrum_analyzer: SpectrumAnalyzer, signal: DataArray, time_interval: float
) -> list[FrequencyBin]:
    """Calculate the FFT of a real signal.

    Args:
        spectrum_analyzer: The analyzer instance to perform FFT
        signal: Input signal data array to analyze
        time_interval: Time interval between samples

    Returns:
        A list of FrequencyBin objects containing the spectrum components
    """

    return spectrum_analyzer.get_signal_spectrum(signal, time_interval)
