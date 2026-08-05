import numpy as np
import logging

class AudioDspFilter:
    """
    Onboard Acoustic Prop-Noise Spectral Subtraction Filter (DSP Core).
    Applies real-time Digital Signal Processing (spectral subtraction) to filter out
    the high-frequency whine of drone propellers (usually peaks between 300Hz - 600Hz)
    to isolate and clean up the user's voice command stream.
    """
    def __init__(self, prop_rpm_freq=450.0, sample_rate=16000):
        self.logger = logging.getLogger("AudioDspFilter")
        self.prop_freq = prop_rpm_freq
        self.sample_rate = sample_rate
        self.logger.info(f"DSP CORE: Prop-noise band-stop filter initialized at target peak: {self.prop_freq}Hz")

    def denoise_audio_chunk(self, raw_audio_data):
        """
        Processes a raw 16kHz 16-bit mono PCM audio buffer.
        Applies a digital band-stop (notch) filter to suppress propeller noise harmonics.
        """
        try:
            if raw_audio_data is None or len(raw_audio_data) < 256:
                return raw_audio_data

            # Convert raw bytes to Float32 array
            signal = np.frombuffer(raw_audio_data, dtype=np.int16).astype(np.float32)
            
            # Apply Fast Fourier Transform (FFT) to convert to frequency domain
            fft_spectrum = np.fft.rfft(signal)
            frequencies = np.fft.rfftfreq(len(signal), d=1.0/self.sample_rate)
            
            # Define notch filter bandwidth around propeller whine (e.g. +/- 50Hz)
            notch_bandwidth = 50.0
            prop_harmonics = [self.prop_freq, self.prop_freq * 2.0] # Suppress fundamental + 1st harmonic
            
            for center_freq in prop_harmonics:
                lower_bound = center_freq - notch_bandwidth
                upper_bound = center_freq + notch_bandwidth
                
                # Zero-out the magnitude of frequencies inside the propeller noise band
                mask = (frequencies >= lower_bound) & (frequencies <= upper_bound)
                fft_spectrum[mask] *= 0.05 # Attenuate by 95%
                
            # Apply Inverse FFT (IFFT) to convert back to time-domain audio
            clean_signal = np.fft.irfft(fft_spectrum)
            
            # Convert back to raw 16-bit PCM bytes
            clean_bytes = np.clip(clean_signal, -32768, 32767).astype(np.int16).tobytes()
            return clean_bytes
            
        except Exception as e:
            self.logger.error(f"DSP filter exception: {e}")
            return raw_audio_data
