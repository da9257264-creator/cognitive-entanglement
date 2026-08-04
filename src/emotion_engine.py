import cv2

class EmotionEngine:
    """
    Analyzes mouth, eyebrow, and eye aspect parameters to determine the pilot's mood.
    Modulates drone safety distances (backs off on fear/anger) and triggers fun behaviors (smiles).
    """
    def __init__(self, config):
        self.enabled = config["emotions"]["facial_expression_tracking"]
        self.safety_dist_fear = config["emotions"]["safety_distance_scale_fear"]
        self.smile_action = config["emotions"]["smile_action"]
        self.current_emotion = "NEUTRAL"

    def analyze_mood(self, landmarks):
        if not self.enabled:
            return "NEUTRAL", 1.0

        # Calculate landmark relationships
        # 1. Mouth Smile Index: distance between mouth corners vs lip separation
        lip_top = landmarks[13]
        lip_bottom = landmarks[14]
        mouth_l = landmarks[61]
        mouth_r = landmarks[291]
        
        mouth_width = self._dist(mouth_l, mouth_r)
        lip_sep = self._dist(lip_top, lip_bottom)
        
        smile_ratio = mouth_width / (lip_sep + 1e-6)

        # 2. Eyebrow raise (Surprise/Fear) vs furrowing (Anger)
        eyebrow_l = landmarks[70]
        eyebrow_r = landmarks[300]
        forehead = landmarks[10]
        
        eyebrow_height = (self._dist(eyebrow_l, forehead) + self._dist(eyebrow_r, forehead)) / 2.0

        # Simple classification heuristics
        scale_factor = 1.0
        if smile_ratio > 3.8 and lip_sep < 0.05:
            self.current_emotion = "HAPPY"
        elif eyebrow_height < 0.12:
            self.current_emotion = "ANGER"
            scale_factor = self.safety_dist_fear # Force drone further away
        elif eyebrow_height > 0.22:
            self.current_emotion = "SURPRISE/FEAR"
            scale_factor = self.safety_dist_fear # Force drone further away
        else:
            self.current_emotion = "NEUTRAL"

        return self.current_emotion, scale_factor

    def _dist(self, p1, p2):
        return ((p1.x - p2.x)**2 + (p1.y - p2.y)**2)**0.5

    def draw_emotion_hud(self, frame):
        color_map = {
            "HAPPY": (0, 255, 0),
            "ANGER": (0, 0, 255),
            "SURPRISE/FEAR": (0, 165, 255),
            "NEUTRAL": (200, 200, 200)
        }
        color = color_map.get(self.current_emotion, (255, 255, 255))
        cv2.putText(frame, f"PILOT MOOD: {self.current_emotion}", (50, 70), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
        return frame
