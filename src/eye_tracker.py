import cv2
import time
import logging

try:
    import mediapipe as mp
    if not hasattr(mp, "solutions"):
        raise AttributeError("solutions API unavailable")
    MEDIAPIPE_AVAILABLE = True
except (ImportError, AttributeError):
    MEDIAPIPE_AVAILABLE = False

class EyeTracker:
    def __init__(self, ear_thresh=0.22, dot_max=0.4, dash_max=1.5, char_space=1.8, word_space=3.5):
        self.logger = logging.getLogger("EyeTracker")
        if not MEDIAPIPE_AVAILABLE:
            self.logger.warning("MediaPipe solutions unavailable on this environment. Local eye tracking is disabled.")
            return

        self.mp_face = mp.solutions.face_mesh
        self.face_mesh = self.mp_face.FaceMesh(max_num_faces=1, refine_landmarks=True)
        
        self.ear_thresh = ear_thresh
        self.dot_max = dot_max
        self.dash_max = dash_max
        self.char_space = char_space
        self.word_space = word_space
        
        self.blink_start_time = None
        self.open_start_time = time.time()
        self.is_closed = False
        
        self.morse_queue = ""
        self.decoded_word = ""
        
        self.MORSE_DICTIONARY = {
            ".-": "ALTITUDE_UP",
            "-.": "ALTITUDE_DOWN",
            "...": "SAFETY_STOP",
            "---": "GO_HOME",
            "..": "START_FOLLOW",
            "--": "MANUAL_MODE",
            "-.-.": "HANDOFF_DONE"
        }

    def calculate_ear(self, landmarks, eye_indices):
        v1 = self.distance(landmarks[eye_indices[1]], landmarks[eye_indices[5]])
        v2 = self.distance(landmarks[eye_indices[2]], landmarks[eye_indices[4]])
        h = self.distance(landmarks[eye_indices[0]], landmarks[eye_indices[3]])
        return (v1 + v2) / (2.0 * h)

    def distance(self, p1, p2):
        return ((p1.x - p2.x)**2 + (p1.y - p2.y)**2)**0.5

    def process_frame(self, frame):
        if not MEDIAPIPE_AVAILABLE:
            return frame, "NONE"

        rgb_img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(rgb_img)
        
        eye_closed = False
        current_time = time.time()
        command_out = "NONE"

        if results.multi_face_landmarks:
            lms = results.multi_face_landmarks[0].landmark
            
            left_eye_indices = [362, 385, 387, 263, 373, 380]
            right_eye_indices = [33, 160, 158, 133, 153, 144]
            
            left_ear = self.calculate_ear(lms, left_eye_indices)
            right_ear = self.calculate_ear(lms, right_eye_indices)
            avg_ear = (left_ear + right_ear) / 2.0
            
            color = (0, 255, 0) if avg_ear > self.ear_thresh else (0, 0, 255)
            cv2.putText(frame, f"EAR: {avg_ear:.2f}", (50, 140), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
            
            if avg_ear < self.ear_thresh:
                eye_closed = True
                
            if eye_closed and not self.is_closed:
                self.is_closed = True
                self.blink_start_time = current_time
            elif not eye_closed and self.is_closed:
                self.is_closed = False
                blink_duration = current_time - self.blink_start_time
                self.open_start_time = current_time
                
                if self.dot_max < blink_duration <= self.dash_max:
                    self.morse_queue += "-"
                elif blink_duration <= self.dot_max:
                    self.morse_queue += "."
            
            if not self.is_closed:
                open_duration = current_time - self.open_start_time
                if len(self.morse_queue) > 0 and open_duration > self.char_space:
                    char = self.MORSE_DICTIONARY.get(self.morse_queue, "?")
                    if char != "?":
                        self.decoded_word = char
                        command_out = char
                    else:
                        self.decoded_word = "[ERROR]"
                    self.morse_queue = ""
                    
        cv2.putText(frame, f"Morse Queue: {self.morse_queue}", (50, 175), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)
        cv2.putText(frame, f"Decoded Morse: {self.decoded_word}", (50, 205), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 255), 2)
                    
        return frame, command_out
