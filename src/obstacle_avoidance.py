import cv2
import numpy as np
import logging

class ObstacleAvoidance:
    """
    Advanced 3D Sector Density Blockade Sensing & Path Recovery System.
    Senses obstacles in Front, Up, and Down hemispheres. If a path is blocked,
    it dynamically modulates speed and height, bypasses the obstacle,
    and then automatically recovers the original path and tracking speed.
    """
    def __init__(self, config):
        self.enabled = config.get("avoidance", {}).get("enabled", True)
        self.safety_dist = config.get("avoidance", {}).get("safety_distance", 1.0)
        self.reaction_gain = config.get("avoidance", {}).get("reaction_gain", 1.5)
        
        # State registers for path memory & recovery
        self.is_bypassing = False
        self.pre_blockade_speed = {"vx": 0.0, "vy": 0.0, "vz": 0.0, "vyaw": 0.0}
        self.recovered_path_count = 0
        
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger("ObstacleAvoidance")

    def sense_blockades(self, frame):
        """
        Scans frames for blockades across three vertical sectors:
        - Front Sector (center viewport)
        - Up Sector (top quarter of frame)
        - Down Sector (bottom quarter of frame)
        Returns blockade status dictionary with densities (0.0 to 1.0).
        """
        if not self.enabled or frame is None:
            return {"front": 0.0, "up": 0.0, "down": 0.0}

        h, w, c = frame.shape
        
        # Segment vertical sectors
        up_zone = frame[0:int(h*0.25), int(w*0.2):int(w*0.8)]
        front_zone = frame[int(h*0.25):int(h*0.75), int(w*0.25):int(w*0.75)]
        down_zone = frame[int(h*0.75):h, int(w*0.2):int(w*0.8)]

        # Calculate hazard densities (high brightness/clutter representation)
        up_density = np.mean(up_zone) / 255.0
        front_density = np.mean(front_zone) / 255.0
        down_density = np.mean(down_zone) / 255.0

        # Draw overlays representing vertical radar arrays
        cv2.rectangle(frame, (int(w*0.2), 0), (int(w*0.8), int(h*0.25)), (0, 0, 255) if up_density > 0.6 else (0, 255, 0), 2)
        cv2.rectangle(frame, (int(w*0.25), int(h*0.25)), (int(w*0.75), int(h*0.75)), (0, 0, 255) if front_density > 0.6 else (0, 255, 0), 2)
        cv2.rectangle(frame, (int(w*0.2), int(h*0.75)), (int(w*0.8), h), (0, 0, 255) if down_density > 0.6 else (0, 255, 0), 2)

        cv2.putText(frame, f"UP SENSOR: {up_density:.2f}", (10, 300), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1)
        cv2.putText(frame, f"FRONT SENSOR: {front_density:.2f}", (10, 320), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1)
        cv2.putText(frame, f"DOWN SENSOR: {down_density:.2f}", (10, 340), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1)

        return {"front": front_density, "up": up_density, "down": down_density}

    def compute_safe_vectors(self, block_data, target_vectors):
        """
        Dynamically adjusts tracking speeds and altitudes to steer around blockades.
        Once the path is clear, automatically restores original user speeds and tracking.
        """
        safe_vectors = target_vectors.copy()
        
        front_blocked = block_data["front"] > 0.6
        up_blocked = block_data["up"] > 0.6
        down_blocked = block_data["down"] > 0.6

        if front_blocked:
            if not self.is_bypassing:
                # Store pre-blockade trajectory parameters into path memory
                self.is_bypassing = True
                self.pre_blockade_speed = target_vectors.copy()
                self.logger.info(f"Blockade sensed ahead! Backing up previous trajectory: {self.pre_blockade_speed}")

            # Slow down forward tracking speed
            safe_vectors["vx"] = -0.15 # Slow deceleration/retreat
            
            # Decide on alternative vertical bypass path (Up or Down)
            if not up_blocked:
                # Climb over blockade
                safe_vectors["vz"] = self.reaction_gain * 0.4
                self.logger.info("Auto-steering UP to climb over blockade.")
            elif not down_blocked:
                # Dive under blockade
                safe_vectors["vz"] = -self.reaction_gain * 0.4
                self.logger.info("Auto-steering DOWN to dive under blockade.")
            else:
                # Total blockade - halt and hover
                safe_vectors["vx"] = 0.0
                safe_vectors["vy"] = 0.0
                safe_vectors["vz"] = 0.0
                safe_vectors["vyaw"] = 0.0
                self.logger.warn("COMPLETE 3D BLOCKADE! Drone holding position.")
                
        else:
            # Path is clear!
            if self.is_bypassing:
                # Overcoming phase: Recover previous path speed
                self.logger.info("Path cleared. Overcoming blockade. Recovering previous flight speed and target trajectories.")
                safe_vectors = self.pre_blockade_speed.copy()
                self.is_bypassing = False # Reset registers
                
        return safe_vectors
