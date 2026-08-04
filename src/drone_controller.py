import time
import math
import logging

class DroneController:
    """
    Unified Drone Controller supporting Simulator, DJI Tello, and PX4/MAVLink backends.
    Supports a single main unit or can serve as an instance for swarm agents.
    """
    def __init__(self, mode="simulator", drone_id=1):
        self.mode = mode.lower()
        self.drone_id = drone_id
        self.connected = False
        self.is_flying = False
        
        # Telemetry variables
        self.position = {"x": 0.0, "y": 0.0, "z": 0.0}
        self.yaw = 0.0
        self.battery = 100
        self.speed = 0.0
        self.flight_mode = "LANDED"
        
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(f"Drone-{self.drone_id}")
        
    def connect(self):
        self.logger.info(f"Connecting in '{self.mode}' mode...")
        if self.mode == "simulator":
            self.connected = True
        elif self.mode == "tello":
            try:
                from djitellopy import Tello
                self.tello = Tello()
                self.tello.connect()
                self.battery = self.tello.get_battery()
                self.connected = True
            except Exception as e:
                self.logger.error(f"Tello connection failed: {e}. Falling back to simulator.")
                self.mode = "simulator"
                self.connected = True
        elif self.mode == "px4":
            try:
                from pymavlink import mavutil
                # Connect to SITL or telemetry link
                self.connection = mavutil.mavlink_connection('udp:127.0.0.1:14550')
                self.connection.wait_heartbeat()
                self.connected = True
            except Exception as e:
                self.logger.error(f"PX4 connection failed: {e}. Falling back to simulator.")
                self.mode = "simulator"
                self.connected = True
        
        self.logger.info("Connection established.")
        return self.connected

    def takeoff(self):
        if not self.connected: return
        self.logger.info("Arming & TAKEOFF initiated.")
        self.is_flying = True
        self.flight_mode = "HOVERING"
        if self.mode == "tello":
            self.tello.takeoff()

    def land(self):
        if not self.connected: return
        self.logger.info("LAND sequence active.")
        self.is_flying = False
        self.flight_mode = "LANDED"
        self.position = {"x": 0.0, "y": 0.0, "z": 0.0}
        if self.mode == "tello":
            self.tello.land()

    def stop(self):
        """Halts all speeds immediately."""
        self.logger.info("HOLD / Emergency Hover.")
        self.flight_mode = "HOVERING"
        self.speed = 0.0
        if self.mode == "tello":
            self.tello.send_rc_control(0, 0, 0, 0)

    def set_velocities(self, vx, vy, vz, vyaw):
        if not self.is_flying: return
        self.flight_mode = "GUIDED"
        self.speed = math.sqrt(vx**2 + vy**2 + vz**2)
        
        if self.mode == "simulator":
            self.position["x"] += vx * 0.1
            self.position["y"] += vy * 0.1
            self.position["z"] += vz * 0.1
            self.yaw += vyaw * 0.1
            
        elif self.mode == "tello":
            tello_pitch = int(max(min(vx * 100, 100), -100))
            tello_roll = int(max(min(vy * 100, 100), -100))
            tello_throttle = int(max(min(vz * 100, 100), -100))
            tello_yaw = int(max(min(vyaw * 100, 100), -100))
            self.tello.send_rc_control(tello_roll, tello_pitch, tello_throttle, tello_yaw)

    def go_to(self, x, y, z):
        if not self.is_flying: return
        self.logger.info(f"Navigating to waypoint: ({x}, {y}, {z})")
        self.flight_mode = "NAVIGATING"
        self.position = {"x": x, "y": y, "z": z}

    def get_telemetry(self):
        if self.mode == "tello" and self.connected:
            try:
                self.battery = self.tello.get_battery()
                self.position["z"] = self.tello.get_height() / 100.0
            except:
                pass
        return {
            "drone_id": self.drone_id,
            "connected": self.connected,
            "is_flying": self.is_flying,
            "position": self.position,
            "yaw": round(self.yaw, 2),
            "battery": self.battery,
            "speed": round(self.speed, 2),
            "flight_mode": self.flight_mode
        }
