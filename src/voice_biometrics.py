import numpy as np
import logging

class VoiceBiometrics:
    """
    Voice Biometric Verification Layer (Speaker Recognition).
    Extracts acoustic spectral footprints (frequency pitch distribution,
    spectral centroid, and energy envelope) from voice commands to verify
    if the spoken command belongs to the registered pilot.
    """
    def __init__(self, config):
        self.enabled = config.get("security", {}).get("voice_biometrics_enabled", True)
        self.match_threshold = config.get("security", {}).get("voice_signature_threshold", 0.15)
        
        # Stored reference signature for the authorized operator
        # (Pitch centroid, Spectral variance, Crest factor/energy ratio)
        self.registered_voice_profile = np.array([125.0, 45.0, 12.5]) # Custom profile baseline (in Hz/ratios)
        self.is_voice_enrolled = True
        
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger("VoiceBiometrics")

    def enroll_voice(self, audio_data, sample_rate=16000):
        """
        Enrolls the authorized operator's voice by computing their unique 
        vocal signature from an audio sample.
        """
        signature = self._extract_vocal_signature(audio_data, sample_rate)
        if signature is not None:
            self.registered_voice_profile = signature
            self.is_voice_enrolled = True
            self.logger.info(f"Voice footprint enrolled successfully: {self.registered_voice_profile}")
            return True
        return False

    def verify_speaker(self, audio_data, sample_rate=16000):
        """
        Verifies if the incoming audio matched the registered owner's voice print.
        """
        if not self.enabled or not self.is_voice_enrolled:
            return True # Bypassed or not enrolled

        input_signature = self._extract_vocal_signature(audio_data, sample_rate)
        if input_signature is None:
            return False

        # Calculate Euclidean distance between input and enrolled footprints
        distance = np.linalg.norm(input_signature - self.registered_voice_profile) / np.linalg.norm(self.registered_voice_profile)
        
        self.logger.info(f"Speaker verification match distance: {distance:.4f} (Threshold: {self.match_threshold})")
        
        # If difference is below our safety margin, speaker is authorized
        return distance < self.match_threshold

    def _extract_vocal_signature(self, audio_data, sample_rate):
        """
        Extracts robust frequency-domain acoustic features from a raw PCM audio buffer.
        Computes Fundamental Frequency estimate (Pitch), Spectral Centroid, and Roll-off.
        """
        try:
            if len(audio_data) < 512:
                return None
                
            # Convert raw bytes or list into numpy array
            signal = np.frombuffer(audio_data, dtype=np.int16) if isinstance(audio_data, bytes) else np.array(audio_data, dtype=np.float32)
            
            # Apply Fast Fourier Transform (FFT)
            fft_data = np.abs(np.fft.rfft(signal))
            frequencies = np.fft.rfftfreq(len(signal), d=1.0/sample_rate)
            
            # Find fundamental pitch centroid
            peak_idx = np.argmax(fft_data)
            fundamental_pitch = frequencies[peak_idx]
            
            # Compute Spectral Centroid (brightness / vowel shape of voice)
            spectral_centroid = np.sum(frequencies * fft_data) / (np.sum(fft_data) + 1e-6)
            
            # Compute Spectral Spread (variance of frequencies)
            spectral_variance = np.sqrt(np.sum(((frequencies - spectral_centroid)**2) * fft_data) / (np.sum(fft_data) + 1e-6))
            
            # Normalize and return vocal footprint vector
            return np.array([fundamental_pitch, spectral_centroid / 10.0, spectral_variance / 10.0])
        except Exception as e:
            self.logger.error(f"Error extracting acoustic signature: {e}")
            return None
