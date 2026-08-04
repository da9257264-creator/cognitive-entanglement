import cv2
import logging
import math

try:
    import mediapipe as mp
    if not hasattr(mp, "solutions"):
        raise AttributeError("solutions API unavailable")
    MEDIAPIPE_AVAILABLE = True
except (ImportError, AttributeError):
    MEDIAPIPE_AVAILABLE = False

class GestureDetector:
    def __init__(self, min_confidence=0.7, cross_threshold=0.08):
        self.logger = logging.getLogger("GestureDetector")
        if not MEDIAPIPE_AVAILABLE:
            self.logger.warning("MediaPipe solutions unavailable on this environment. Local camera CV is disabled.")
            return

        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=min_confidence,
            min_tracking_confidence=min_confidence
        )
        self.mp_draw = mp.solutions.drawing_utils
        self.cross_threshold = cross_threshold

    def process_frame(self, frame):
        if not MEDIAPIPE_AVAILABLE:
            return frame, "NONE"

        h, w, c = frame.shape
        img_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(img_rgb)
        
        gesture = "NONE"
        left_wrist, right_wrist = None, None
        
        if results.multi_hand_landmarks:
            num_hands = len(results.multi_hand_landmarks)
            
            # Check for double hands crossed
            if num_hands == 2:
                for idx, hand_lms in enumerate(results.multi_hand_landmarks):
                    self.mp_draw.draw_landmarks(frame, hand_lms, self.mp_hands.HAND_CONNECTIONS)
                    hand_label = results.multi_handedness[idx].classification[0].label
                    wrist = hand_lms.landmark[self.mp_hands.HandLandmark.WRIST]
                    
                    if hand_label == "Left" or hand_label == "Left-handed":
                        left_wrist = (wrist.x, wrist.y, wrist.z)
                    else:
                        right_wrist = (wrist.x, wrist.y, wrist.z)
                
                if left_wrist and right_wrist:
                    dx = abs(left_wrist[0] - right_wrist[0])
                    dy = abs(left_wrist[1] - right_wrist[1])
                    dist = math.sqrt(dx**2 + dy**2)
                    
                    if dist < self.cross_threshold and left_wrist[0] < right_wrist[0]:
                        gesture = "CROSS_HANDS"
                        cv2.putText(frame, "HOLD ACTIVE: CROSSED WRISTS", (50, 90), 
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 3)

            # Single-hand tracking
            if num_hands == 1 and gesture == "NONE":
                hand_lms = results.multi_hand_landmarks[0]
                self.mp_draw.draw_landmarks(frame, hand_lms, self.mp_hands.HAND_CONNECTIONS)
                
                fingers = []
                landmarks = hand_lms.landmark
                
                # Thumb (Horizontal relative direction)
                if landmarks[4].x < landmarks[3].x:
                    fingers.append(1)
                else:
                    fingers.append(0)
                    
                # Index, Middle, Ring, Pinky
                for tip, pip in [(8, 6), (12, 10), (16, 14), (20, 18)]:
                    if landmarks[tip].y < landmarks[pip].y:
                        fingers.append(1)
                    else:
                        fingers.append(0)
                
                # -------------------------------------------------------------------
                # Sign Language Landmark Mapping:
                # -------------------------------------------------------------------
                # 1. "I Love You" (ILY) Sign -> Thumb, Index, Pinky open. Middle & Ring folded.
                if fingers == [1, 1, 0, 0, 1]:
                    gesture = "ASL_ILY" 
                    cv2.putText(frame, "ASL: I-LOVE-YOU (RETURN HOME)", (50, 90), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                
                # 2. "Victory / Peace" Sign -> Index and Middle open. Others folded.
                elif fingers == [0, 1, 1, 0, 0]:
                    gesture = "ASL_PEACE" 
                    cv2.putText(frame, "ASL: PEACE/V (TAKEOFF)", (50, 90), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                
                # 3. "Shaka / Y" Sign -> Thumb and Pinky open. Others folded.
                elif fingers == [1, 0, 0, 0, 1]:
                    gesture = "ASL_Y" 
                    cv2.putText(frame, "ASL: SHAKA/Y (START FOLLOW)", (50, 90), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                                
                # 4. "Thumbs Up" Sign -> Thumb open. Others completely folded.
                elif fingers == [1, 0, 0, 0, 0]:
                    gesture = "ASL_THUMBS_UP" 
                    cv2.putText(frame, "ASL: THUMBS-UP (CLIMB)", (50, 90), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                                
                # 5. "OK" Sign -> Thumb & Index touching. Middle, Ring, Pinky open.
                elif fingers == [0, 0, 1, 1, 1]:
                    gesture = "ASL_OK" 
                    cv2.putText(frame, "ASL: OK (LAND)", (50, 90), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
                
                # 6. "Wait / Hold" Gesture -> Open palm forward-facing, all fingers extended.
                elif fingers == [1, 1, 1, 1, 1]:
                    gesture = "ASL_WAIT"
                    cv2.putText(frame, "WAIT / HOVER COMMAND ACTIVE", (50, 90), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
                
                # Fallback shapes
                else:
                    total_fingers = sum(fingers)
                    if total_fingers == 0:
                        gesture = "FIST"
                    elif total_fingers == 5:
                        gesture = "OPEN_PALM"
                                
        return frame, gesture
