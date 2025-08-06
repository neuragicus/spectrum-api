""" """

from ..models.input_models import DataArray, FrequencyBin
from ..services.fft import SpectrumAnalyzer


def fft_real(
    spectrum_analyzer: SpectrumAnalyzer, signal: DataArray, time_interval: float
) -> list[FrequencyBin]:
    """
    Wrapper for the endpoint that calculates the FFT or real signal
    :param spectrum_analyzer:
    :return:
    """

    return spectrum_analyzer.get_signal_spectrum(signal, time_interval)
