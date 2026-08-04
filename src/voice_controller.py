import logging
import threading

try:
    import speech_recognition as sr
    PYAUDIO_AVAILABLE = True
except ImportError:
    PYAUDIO_AVAILABLE = False

class VoiceController:
    def __init__(self):
        self.last_command = "NONE"
        self.last_audio_bytes = None
        self.is_running = False
        
        # Acoustic Tuning variables
        self.speed_scale = 1.0 # 0.5 for slow, 1.0 for normal, 1.8 for fast
        self.target_height_offset = 0.0 # Height adjustment offset from voice commands
        
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger("VoiceController")
        
        self.VOICE_COMMAND_MAP = {
            "takeoff": "TAKEOFF",
            "fly": "TAKEOFF",
            "land": "LAND",
            "stop": "STOP",
            "hover": "STOP",
            "panic": "PANIC",
            "emergency": "PANIC",
            "wait": "WAIT",
            "selfie": "SELFIE",
            "find": "FIND",
            "follow": "START_FOLLOW",
            "track": "START_FOLLOW",
            "return home": "GO_HOME",
            "go back": "GO_HOME",
            "handoff complete": "HANDOFF_DONE",
            "delivered": "HANDOFF_DONE",
            "authorize": "SECURE_AUTH",
            "front flip": "FRONT_FLIP",
            "back flip": "BACK_FLIP",
            "flip left": "LEFT_FLIP",
            "flip right": "RIGHT_FLIP",
            "tornado": "TORNADO",
            "dance": "DANCE",
            "glide": "GLIDE",
            "orbit": "ORBIT"
        }

        # Check speech recognition capability
        self.local_enabled = PYAUDIO_AVAILABLE
        if PYAUDIO_AVAILABLE:
            try:
                self.recognizer = sr.Recognizer()
                self.microphone = sr.Microphone()
            except Exception as e:
                self.logger.warning(f"Failed to bind local Microphone (could be missing PyAudio / sound drivers): {e}. Web-based voice tracking is active via browser!")
                self.local_enabled = False

    def start_listening(self):
        if not self.local_enabled:
            self.logger.warning("Local voice listening bypassed. Browser Web Speech API active instead.")
            return
        self.is_running = True
        self.thread = threading.Thread(target=self._listen_loop, daemon=True)
        self.thread.start()
        self.logger.info("Voice Listening system primed.")

    def stop_listening(self):
        self.is_running = False

    def _listen_loop(self):
        while self.is_running:
            try:
                with self.microphone as source:
                    self.logger.info("Vocal input active...")
                    audio = self.recognizer.listen(source, timeout=3, phrase_time_limit=4)
                
                text = self.recognizer.recognize_google(audio).lower()
                self.logger.info(f"Speech decoded: {text}")
                
                # Check for velocity scale and altitude tuning commands
                self._parse_vocal_tuning(text)
                
                for trigger, cmd in self.VOICE_COMMAND_MAP.items():
                    if trigger in text:
                        self.last_command = cmd
                        # Extract raw 16kHz 16-bit mono PCM bytes for biometric matching
                        self.last_audio_bytes = audio.get_raw_data(convert_rate=16000, convert_width=2)
                        self.logger.info(f"Voice action identified: {cmd} with audio footprint.")
                        break
            except Exception:
                continue

    def _parse_vocal_tuning(self, text):
        """
        Parses speed and altitude adjustment directives.
        Example commands: 'speed fast', 'slow down', 'climb higher', 'fly lower'
        """
        # Speed tuning
        if "speed fast" in text or "accelerate" in text:
            self.speed_scale = 1.8
            self.logger.info("Vocal speed modifier: FAST (1.8x)")
        elif "speed slow" in text or "slow down" in text:
            self.speed_scale = 0.5
            self.logger.info("Vocal speed modifier: SLOW (0.5x)")
        elif "speed normal" in text or "normalize speed" in text:
            self.speed_scale = 1.0
            self.logger.info("Vocal speed modifier: NORMAL (1.0x)")

        # Height tuning
        if "climb higher" in text or "go up" in text:
            self.target_height_offset += 0.5
            self.logger.info(f"Vocal height modifier: CLIMB (+0.5m, current total: {self.target_height_offset})")
        elif "fly lower" in text or "go down" in text:
            self.target_height_offset -= 0.5
            self.logger.info(f"Vocal height modifier: DESCEND (-0.5m, current total: {self.target_height_offset})")

    def get_latest_command(self):
        cmd = self.last_command
        audio = self.last_audio_bytes
        self.last_command = "NONE"
        self.last_audio_bytes = None
        return cmd, audio
