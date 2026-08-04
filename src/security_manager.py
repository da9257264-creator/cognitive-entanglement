import cv2
import numpy as np

class SecurityManager:
    """
    Biometric Authorization layer.
    Extracts high-dimensional spatial land-mark proportions from FaceMesh
    and confirms if the current pilot matches the Authorized Owner Profile.
    """
    def __init__(self, config):
        self.enabled = config["security"]["biometrics_enabled"]
        self.auth_threshold = config["security"]["auth_facial_ratio_threshold"]
        self.owner_profile = config["security"]["authorized_user_profile"]
        self.is_authorized = False

    def authorize_operator(self, landmarks):
        """
        Validates operator face configuration against profile metrics.
        landmarks: list of normalized FaceMesh landmarks
        """
        if not self.enabled:
            self.is_authorized = True
            return True

        # Calculate ratios to account for screen depth variance
        # R1: Vertical eye spacing to Mouth width
        eye_dist = self._landmark_distance(landmarks[33], landmarks[263]) # Outer eyes
        mouth_width = self._landmark_distance(landmarks[61], landmarks[291]) # Mouth edges
        eye_to_mouth = eye_dist / (mouth_width + 1e-6)

        # R2: Jaw depth to eyebrow spacing
        jaw_depth = self._landmark_distance(landmarks[152], landmarks[10]) # Chin to forehead
        eyebrow_dist = self._landmark_distance(landmarks[70], landmarks[300]) # Eyebrows
        jaw_to_eyebrow = jaw_depth / (eyebrow_dist + 1e-6)

        # Compute difference from stored profile config
        diff_r1 = abs(eye_to_mouth - self.owner_profile["eye_to_mouth_ratio"])
        diff_r2 = abs(jaw_to_eyebrow - self.owner_profile["jaw_to_eyebrow_ratio"])

        if diff_r1 < self.auth_threshold and diff_r2 < self.auth_threshold:
            self.is_authorized = True
        else:
            self.is_authorized = False

        return self.is_authorized

    def _landmark_distance(self, p1, p2):
        return ((p1.x - p2.x)**2 + (p1.y - p2.y)**2 + (p1.z - p2.z)**2)**0.5

    def draw_security_hud(self, frame):
        status = "AUTHORIZED PILOT" if self.is_authorized else "SECURE LOCK: UNAUTHORIZED"
        color = (0, 255, 0) if self.is_authorized else (0, 0, 255)
        
        # Security scanner frame border
        cv2.putText(frame, f"SEC-LOCK: {status}", (50, 40), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
        return frame
