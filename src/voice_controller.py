import logging
import threading

try:
    import speech_recognition as sr
    PYAUDIO_AVAILABLE = True
except ImportError:
    PYAUDIO_AVAILABLE = False

class VoiceController:
    """
    Global Multi-Lingual Voice Command Processing Engine.
    Leverages advanced speech models supporting over 120 world languages.
    Maps localized vocal commands in English, Spanish, Chinese, French, German,
    Arabic, and Hindi to unified flight state triggers.
    """
    def __init__(self, target_lang="en-US"):
        self.last_command = "NONE"
        self.last_audio_bytes = None
        self.is_running = False
        
        # Current active language code (e.g., 'en-US', 'zh-CN', 'es-ES', 'ar-EG')
        self.target_lang = target_lang
        
        # Acoustic Tuning variables
        self.speed_scale = 1.0 
        self.target_height_offset = 0.0 
        
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger("VoiceController")
        
        # Global Multi-Lingual Command Dictionary (Supports all major world pilots)
        self.GLOBAL_COMMAND_DICTIONARY = {
            # --- English commands ---
            "takeoff": "TAKEOFF", "fly": "TAKEOFF", "land": "LAND", "stop": "STOP", "hover": "STOP",
            "follow": "START_FOLLOW", "track": "START_FOLLOW", "return home": "GO_HOME", "go back": "GO_HOME",
            "handoff complete": "HANDOFF_DONE", "wait": "WAIT", "selfie": "SELFIE", "find": "FIND", "panic": "PANIC",
            "front flip": "FRONT_FLIP", "back flip": "BACK_FLIP", "tornado": "TORNADO", "dance": "DANCE",
            "formation line": "FORMATION_LINE", "formation orbit": "FORMATION_ORBIT", "formation normal": "FORMATION_V",
            
            # --- Spanish commands (Español) ---
            "despegar": "TAKEOFF", "vuela": "TAKEOFF", "aterrizar": "LAND", "para": "STOP", "espera": "WAIT",
            "sigueme": "START_FOLLOW", "regresar": "GO_HOME", "voltear": "FRONT_FLIP", "gira": "TORNADO",
            
            # --- Chinese commands (中文) ---
            "起飞": "TAKEOFF", "飞行": "TAKEOFF", "降落": "LAND", "停止": "STOP", "悬停": "STOP",
            "跟随": "START_FOLLOW", "返航": "GO_HOME", "等待": "WAIT", "自拍": "SELFIE", "翻滚": "FRONT_FLIP",
            "旋风": "TORNADO", "跳舞": "DANCE", "寻找": "FIND", "编队": "FORMATION_LINE",
            
            # --- French commands (Français) ---
            "decollage": "TAKEOFF", "vole": "TAKEOFF", "atterrir": "LAND", "arrete": "STOP", "attends": "WAIT",
            "suis moi": "START_FOLLOW", "retourne": "GO_HOME", "salto": "FRONT_FLIP", "tourbillon": "TORNADO",
            
            # --- German commands (Deutsch) ---
            "starten": "TAKEOFF", "fliegen": "TAKEOFF", "landen": "LAND", "stoppen": "STOP", "warten": "WAIT",
            "folgen": "START_FOLLOW", "zuruck": "GO_HOME", "salto": "FRONT_FLIP", "wirbel": "TORNADO",
            
            # --- Arabic commands (العربية) ---
            "اقلاع": "TAKEOFF", "طير": "TAKEOFF", "هبوط": "LAND", "توقف": "STOP", "اتبعني": "START_FOLLOW",
            "ارجع": "GO_HOME", "انتظر": "WAIT", "سيلفي": "SELFIE", "دوران": "TORNADO",
            
            # --- Hindi commands (हिन्दी) ---
            "उड़ान": "TAKEOFF", "उड़ो": "TAKEOFF", "लैंड": "LAND", "रुको": "STOP", "पीछा": "START_FOLLOW",
            "वापस": "GO_HOME", "इंतजार": "WAIT", "सेल्फी": "SELFIE", "चक्रवात": "TORNADO"
        }

        # Check speech recognition capability
        self.local_enabled = PYAUDIO_AVAILABLE
        if PYAUDIO_AVAILABLE:
            try:
                self.recognizer = sr.Recognizer()
                self.microphone = sr.Microphone()
            except Exception as e:
                self.logger.warning(f"Failed to bind local Microphone: {e}. Web-based voice tracking active.")
                self.local_enabled = False

    def start_listening(self):
        if not self.local_enabled:
            return
        self.is_running = True
        self.thread = threading.Thread(target=self._listen_loop, daemon=True)
        self.thread.start()
        self.logger.info(f"Voice Listening system primed for language: {self.target_lang}")

    def stop_listening(self):
        self.is_running = False

    def _listen_loop(self):
        while self.is_running:
            try:
                with self.microphone as source:
                    audio = self.recognizer.listen(source, timeout=3, phrase_time_limit=4)
                
                # Perform Speech-To-Text in target language
                text = self.recognizer.recognize_google(audio, language=self.target_lang).lower()
                self.logger.info(f"Speech decoded [{self.target_lang}]: {text}")
                
                # Parse velocity scale and altitude tuning commands
                self._parse_vocal_tuning(text)
                
                for trigger, cmd in self.GLOBAL_COMMAND_DICTIONARY.items():
                    if trigger in text:
                        self.last_command = cmd
                        self.last_audio_bytes = audio.get_raw_data(convert_rate=16000, convert_width=2)
                        self.logger.info(f"Global Voice Action matched: {cmd}")
                        break
            except Exception:
                continue

    def _parse_vocal_tuning(self, text):
        # Speed tuning
        if "speed fast" in text or "accelerate" in text or "velocidad rapida" in text or "加速" in text:
            self.speed_scale = 1.8
        elif "speed slow" in text or "slow down" in text or "velocidad lenta" in text or "减速" in text:
            self.speed_scale = 0.5
        elif "speed normal" in text or "normalize" in text or "velocidad normal" in text or "正常速度" in text:
            self.speed_scale = 1.0

        # Height tuning
        if "climb higher" in text or "go up" in text or "subir" in text or "升高" in text:
            self.target_height_offset += 0.5
        elif "fly lower" in text or "go down" in text or "bajar" in text or "降低" in text:
            self.target_height_offset -= 0.5

    def get_latest_command(self):
        cmd = self.last_command
        audio = self.last_audio_bytes
        self.last_command = "NONE"
        self.last_audio_bytes = None
        return cmd, audio
