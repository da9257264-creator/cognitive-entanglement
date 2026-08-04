import logging

class EnrollmentWizard:
    """
    Interactive Voice & Visual Setup Wizard.
    Guides a new user step-by-step to calibrate their facial biometrics,
    vocal biometrics, and test basic gestures before actual takeoff.
    Makes the advanced framework incredibly easy to use for beginners!
    """
    def __init__(self):
        self.current_step = "WELCOME" # STEPS: WELCOME, FACE_SCAN, VOICE_SCAN, GESTURE_CHECK, READY
        self.step_logs = {
            "WELCOME": "Welcome! Press 'Start Calibration' to begin your safety setup.",
            "FACE_SCAN": "Please look directly at the camera so Phone A can scan your facial geometry.",
            "VOICE_SCAN": "Face registered. Now say clearly: 'Authorize Drone' to calibrate your voice print.",
            "GESTURE_CHECK": "Voice enrolled. Finally, show the ASL Peace (V) sign to confirm camera control.",
            "READY": "Setup complete! You are the authorized operator. Speak or gesture to fly safely!"
        }
        self.logger = logging.getLogger("EnrollmentWizard")

    def advance_step(self, trigger_condition):
        """Advances the user through the setup flow when conditions are satisfied."""
        if self.current_step == "WELCOME" and trigger_condition == "START":
            self.current_step = "FACE_SCAN"
            return self.get_current_instructions()
            
        elif self.current_step == "FACE_SCAN" and trigger_condition == "FACE_MATCHED":
            self.current_step = "VOICE_SCAN"
            return self.get_current_instructions()
            
        elif self.current_step == "VOICE_SCAN" and trigger_condition == "VOICE_MATCHED":
            self.current_step = "GESTURE_CHECK"
            return self.get_current_instructions()
            
        elif self.current_step == "GESTURE_CHECK" and trigger_condition == "GESTURE_MATCHED":
            self.current_step = "READY"
            return self.get_current_instructions()
            
        return None

    def get_current_instructions(self):
        instruction = self.step_logs.get(self.current_step, "")
        self.logger.info(f"WIZARD STATE: {self.current_step} - {instruction}")
        return {
            "step": self.current_step,
            "instruction": instruction
        }
