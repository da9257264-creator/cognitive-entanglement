import cv2
import numpy as np
import logging

try:
    import mediapipe as mp
    if not hasattr(mp, "solutions"):
        raise AttributeError("solutions API unavailable")
    MEDIAPIPE_AVAILABLE = True
except (ImportError, AttributeError):
    MEDIAPIPE_AVAILABLE = False

class BodyTracker:
    def __init__(self, follow_dist=0.15, tolerance=0.02, motion_thresh=0.03):
        self.logger = logging.getLogger("BodyTracker")
        if not MEDIAPIPE_AVAILABLE:
            self.logger.warning("MediaPipe solutions unavailable on this environment. Local body tracking is disabled.")
            return

        self.mp_pose = mp.solutions.pose
        self.pose = self.mp_pose.Pose(min_detection_confidence=0.7, min_tracking_confidence=0.7)
        self.mp_draw = mp.solutions.drawing_utils
        
        self.follow_dist = follow_dist
        self.tolerance = tolerance
        self.motion_thresh = motion_thresh
        
        self.history = []
        self.moving_state = "STOPPED"

    def process_frame(self, frame):
        if not MEDIAPIPE_AVAILABLE:
            return frame, {"vx": 0.0, "vy": 0.0, "vz": 0.0, "vyaw": 0.0}, "STOPPED"

        h, w, c = frame.shape
        rgb_img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.pose.process(rgb_img)
        
        tracking_vectors = {"vx": 0.0, "vy": 0.0, "vz": 0.0, "vyaw": 0.0}
        
        if results.pose_landmarks:
            self.mp_draw.draw_landmarks(frame, results.pose_landmarks, self.mp_pose.POSE_CONNECTIONS)
            lms = results.pose_landmarks.landmark
            
            nose = lms[self.mp_pose.PoseLandmark.NOSE]
            l_shoulder = lms[self.mp_pose.PoseLandmark.LEFT_SHOULDER]
            r_shoulder = lms[self.mp_pose.PoseLandmark.RIGHT_SHOULDER]
            
            shoulder_width = abs(l_shoulder.x - r_shoulder.x)
            
            offset_x = nose.x - 0.5
            offset_y = nose.y - 0.4
            
            current_pos = np.array([nose.x, nose.y, shoulder_width])
            self.history.append(current_pos)
            if len(self.history) > 10:
                self.history.pop(0)
                
            variance = np.var(self.history, axis=0)
            avg_displacement = np.mean(variance)
            
            if avg_displacement > self.motion_thresh:
                self.moving_state = "MOVING"
            else:
                self.moving_state = "STOPPED"
                
            distance_error = self.follow_dist - shoulder_width
            if abs(distance_error) > self.tolerance:
                tracking_vectors["vx"] = distance_error * 2.5
                
            if abs(offset_x) > 0.05:
                tracking_vectors["vyaw"] = offset_x * 1.8
                
            if abs(offset_y) > 0.05:
                tracking_vectors["vz"] = -offset_y * 1.5
                
            cv2.putText(frame, f"User Motion: {self.moving_state}", (50, 240), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
            
        return frame, tracking_vectors, self.moving_state
