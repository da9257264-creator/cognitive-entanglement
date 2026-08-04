import cv2
import numpy as np
import logging

class ObjectTracker:
    """
    Onboard Visual Object Tracking Engine (ActiveTrack).
    Enables Phone A's camera to lock onto and track specific objects 
    (such as a dog, backpack, ball, or bicycle) based on voice requests from Phone B.
    """
    def __init__(self):
        self.logger = logging.getLogger("ObjectTracker")
        self.is_tracking_target = False
        self.target_class = "NONE"
        self.target_bbox = [0.0, 0.0, 0.0, 0.0] # [x, y, w, h] normalized
        
        # COCO dataset classes supported for voice-guided ActiveTrack
        self.SUPPORTED_CLASSES = ["person", "bicycle", "car", "cat", "dog", "backpack", "umbrella", "ball"]

    def set_target(self, class_name):
        class_name = class_name.lower()
        if class_name in self.SUPPORTED_CLASSES:
            self.target_class = class_name
            self.is_tracking_target = True
            self.logger.info(f"ACTIVETRACK: Locked target class to: '{self.target_class.upper()}'")
            return True
        else:
            self.logger.warning(f"Class '{class_name}' is not in supported tracking datasets.")
            return False

    def cancel_tracking(self):
        self.is_tracking_target = False
        self.target_class = "NONE"
        self.target_bbox = [0.0, 0.0, 0.0, 0.0]
        self.logger.info("ACTIVETRACK: Visual target tracking cancelled.")

    def track_object_in_frame(self, frame):
        """
        Simulates onboard object detection. 
        Detects simulated bounding boxes for target classes to calculate steering vectors.
        """
        if not self.is_tracking_target or frame is None:
            return frame, {"vx": 0.0, "vyaw": 0.0}

        h, w, c = frame.shape
        
        # Simulate tracking box near center with minor noise
        bx = int(w * 0.45)
        by = int(h * 0.40)
        bw = int(w * 0.15)
        bh = int(h * 0.30)
        
        # Calculate horizontal tracking error
        offset_x = (bx + bw/2.0) / w - 0.5
        
        # Proportional tracking vector adjustments
        control_vectors = {
            "vx": 0.3, # Move forward to keep tracking
            "vyaw": offset_x * 1.5 # Rotate to keep target centered
        }
        
        # Draw bounding box and label
        cv2.rectangle(frame, (bx, by), (bx+bw, by+bh), (0, 165, 255), 2)
        cv2.putText(frame, f"ACTIVETRACK: {self.target_class.upper()} [LOCKED]", 
                    (bx, by - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 165, 255), 2)
        
        return frame, control_vectors
