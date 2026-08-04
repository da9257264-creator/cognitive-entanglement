import math
import time
import logging

class SwarmController:
    """
    Coordinates multi-drone swarm formations.
    Supports dynamic formation shifting (V-SHAPE, LINE, and ORBIT/HELIX)
    triggered via voice command or dashboard control in real-time.
    """
    def __init__(self, swarm_size=3, separation_dist=1.5):
        self.swarm_size = swarm_size
        self.separation_dist = separation_dist
        self.formation_type = "V-SHAPE" # Formations: V-SHAPE, LINE, ORBIT
        self.followers_telemetry = {}
        
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger("SwarmController")
        
        # Initialize followers coordinates
        for i in range(2, swarm_size + 1):
            self.followers_telemetry[i] = {
                "drone_id": i,
                "position": {"x": 0.0, "y": 0.0, "z": 0.0},
                "yaw": 0.0,
                "flight_mode": "LANDED"
            }

    def set_formation(self, formation_name):
        formation_name = formation_name.upper()
        if formation_name in ["V-SHAPE", "LINE", "ORBIT"]:
            self.formation_type = formation_name
            self.logger.info(f"SWARM CORE: Shifted flocking formation to: {self.formation_type}")
            return True
        return False

    def update_swarm_positions(self, leader_pos, leader_yaw, leader_mode):
        """
        Calculates flocking offsets for all followers based on the active formation structure.
        """
        rad_yaw = math.radians(leader_yaw)
        
        for i in range(2, self.swarm_size + 1):
            follower = self.followers_telemetry[i]
            follower["flight_mode"] = leader_mode
            
            side_multiplier = -1.0 if (i % 2 == 0) else 1.0
            
            # Default offset registers
            dx_local = 0.0
            dy_local = 0.0
            dz_local = 0.0
            
            if self.formation_type == "V-SHAPE":
                # Symmetrical V-shape behind the leader
                dx_local = -self.separation_dist # Behind
                dy_local = side_multiplier * self.separation_dist # To the side
                dz_local = 0.0 # Same altitude
                
            elif self.formation_type == "LINE":
                # Horizontal parallel row flanking the leader
                dx_local = 0.0 # Aligned horizontally
                dy_local = side_multiplier * (self.separation_dist * (i-1))
                dz_local = 0.0
                
            elif self.formation_type == "ORBIT":
                # Double helix vertical offset orbit
                # Offset orbits rotating with time
                t = time.time() if 'time' in globals() else 1.0
                angle = (t * 2.0) + (side_multiplier * math.pi)
                dx_local = self.separation_dist * math.cos(angle)
                dy_local = self.separation_dist * math.sin(angle)
                dz_local = side_multiplier * 0.4 # Followers stack slightly above and below
            
            # Map local offsets to global coordinates rotated by leader yaw
            dx_global = dx_local * math.cos(rad_yaw) - dy_local * math.sin(rad_yaw)
            dy_global = dx_local * math.sin(rad_yaw) + dy_local * math.cos(rad_yaw)
            
            follower["position"]["x"] = round(leader_pos["x"] + dx_global, 2)
            follower["position"]["y"] = round(leader_pos["y"] + dy_global, 2)
            follower["position"]["z"] = round(leader_pos["z"] + dz_local, 2)
            follower["yaw"] = leader_yaw

    def get_swarm_telemetry(self):
        return self.followers_telemetry
