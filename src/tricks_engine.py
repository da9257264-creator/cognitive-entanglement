import time
import math
import logging

class TricksEngine:
    """
    Advanced Trick & Maneuver Execution Engine.
    Triggers physical maneuvers on DJI Tello or coordinates continuous
    complex trajectory equations on the PX4 or virtual 3D simulator backends.
    Supports high-performance aeronautical aerobatics (Immelmann, Split-S, Barrel Roll).
    """
    def __init__(self, drone_controller):
        self.drone = drone_controller
        self.logger = logging.getLogger("TricksEngine")

    def execute_trick(self, trick_name):
        self.logger.info(f"COGNITIVE ENTANGLEMENT: Initializing trick: {trick_name.upper()}")
        
        if trick_name == "front_flip":
            self._flip('f')
        elif trick_name == "back_flip":
            self._flip('b')
        elif trick_name == "left_flip":
            self._flip('l')
        elif trick_name == "right_flip":
            self._flip('r')
        elif trick_name == "tornado_spin":
            self._execute_tornado_spin()
        elif trick_name == "victory_wobble":
            self._execute_victory_wobble()
        elif trick_name == "eagle_glide":
            self._execute_eagle_glide()
        elif trick_name == "orbit_carousel":
            self._execute_orbit_carousel()
        elif trick_name == "selfie_orbit":
            self._execute_selfie_orbit()
        elif trick_name == "beacon_chirp":
            self._execute_beacon_chirp()
        elif trick_name == "immelmann_turn":
            self._execute_immelmann_turn()
        elif trick_name == "split_s":
            self._execute_split_s()
        elif trick_name == "barrel_roll":
            self._execute_barrel_roll()
        elif trick_name == "chandelle":
            self._execute_chandelle()
        elif trick_name == "space_station_orbit":
            self._execute_space_station_orbit()
        else:
            self.logger.warning(f"Unrecognized trick profile: {trick_name}")

    def _flip(self, direction):
        if self.drone.mode == "tello":
            try:
                self.drone.tello.flip(direction)
            except Exception as e:
                self.logger.error(f"Physical flip failed: {e}")
        else:
            self.drone.set_velocities(0, 0, 0.8, 0)
            time.sleep(0.5)
            roll = 1.5 if direction == 'r' else -1.5 if direction == 'l' else 0.0
            pitch = 1.5 if direction == 'f' else -1.5 if direction == 'b' else 0.0
            self.drone.set_velocities(pitch, roll, -0.2, 0.0)
            time.sleep(0.6)
            self.drone.stop()

    def _execute_tornado_spin(self):
        for _ in range(15):
            self.drone.set_velocities(0.1, 0, 0.6, 2.0)
            time.sleep(0.1)
        self.drone.stop()

    def _execute_victory_wobble(self):
        for _ in range(2):
            self.drone.set_velocities(0, 0.4, 0, 0)
            time.sleep(0.2)
            self.drone.set_velocities(0, -0.4, 0, 0)
            time.sleep(0.2)
        self.drone.stop()

    def _execute_eagle_glide(self):
        start_time = time.time()
        while time.time() - start_time < 3.0:
            elapsed = time.time() - start_time
            vz_oscillation = 0.5 * math.sin(2.0 * math.pi * 0.5 * elapsed)
            self.drone.set_velocities(0.4, 0.0, vz_oscillation, 0.0)
            time.sleep(0.1)
        self.drone.stop()

    def _execute_orbit_carousel(self):
        start_time = time.time()
        omega = 1.5
        radius = 1.0
        while time.time() - start_time < 4.2:
            elapsed = time.time() - start_time
            vx = -radius * omega * math.sin(omega * elapsed)
            vy = radius * omega * math.cos(omega * elapsed)
            vyaw = omega
            self.drone.set_velocities(vx, vy, 0.0, vyaw)
            time.sleep(0.1)
        self.drone.stop()

    def _execute_selfie_orbit(self):
        self.drone.set_velocities(-0.4, 0.0, 0.2, 0.0)
        time.sleep(1.5)
        self.drone.stop()
        
        start_time = time.time()
        omega = 0.8
        radius = 2.0
        while time.time() - start_time < 4.0:
            elapsed = time.time() - start_time
            vx = -radius * omega * math.sin(omega * elapsed)
            vy = radius * omega * math.cos(omega * elapsed)
            vyaw = omega
            self.drone.set_velocities(vx, vy, 0.0, vyaw)
            time.sleep(0.1)
        self.drone.stop()

    def _execute_beacon_chirp(self):
        for _ in range(3):
            self.drone.set_velocities(0, 0, 0, 1.5)
            time.sleep(0.15)
            self.drone.set_velocities(0, 0, 0, -1.5)
            time.sleep(0.15)
        self.drone.stop()

    def _execute_immelmann_turn(self):
        self.logger.info("AEROBATICS: Commencing IMMELMANN TURN.")
        self.drone.set_velocities(0.3, 0.0, 0.8, 0.0)
        time.sleep(1.5)
        self.drone.set_velocities(0.0, 1.5, 0.0, 2.0)
        time.sleep(0.8)
        self.drone.stop()

    def _execute_split_s(self):
        self.logger.info("AEROBATICS: Commencing SPLIT-S tactical dive.")
        self.drone.set_velocities(0.0, 1.8, 0.0, 0.0)
        time.sleep(0.6)
        self.drone.set_velocities(0.4, 0.0, -0.8, 0.0)
        time.sleep(1.2)
        self.drone.stop()

    def _execute_barrel_roll(self):
        self.logger.info("AEROBATICS: Commencing BARREL ROLL.")
        start_time = time.time()
        while time.time() - start_time < 2.0:
            elapsed = time.time() - start_time
            roll = 1.5 * math.sin(math.pi * elapsed)
            self.drone.set_velocities(0.5, roll, 0.0, 0.0)
            time.sleep(0.1)
        self.drone.stop()

    def _execute_chandelle(self):
        self.logger.info("AEROBATICS: Commencing CHANDELLE climbing turn.")
        self.drone.set_velocities(0.4, 0.0, 0.5, 1.5)
        time.sleep(2.0)
        self.drone.stop()

    def _execute_space_station_orbit(self):
        """Dynamic Keplerian Orbit Sync around virtual Space Station target (JPL Spec)."""
        self.logger.info("AEROBATICS: Commencing SPACE STATION ORBIT SYNC.")
        start_time = time.time()
        omega = 1.2
        radius = 2.5
        while time.time() - start_time < 6.0:
            elapsed = time.time() - start_time
            # Multi-axis sinusoidal orbital equation representing elliptical Keplerian drift
            vx = -radius * omega * math.sin(omega * elapsed)
            vy = radius * omega * math.cos(omega * elapsed)
            vz = 0.3 * math.cos(2 * omega * elapsed) # Stack vertical oscillation (elliptical orbit!)
            vyaw = omega
            self.drone.set_velocities(vx, vy, vz, vyaw)
            time.sleep(0.1)
        self.drone.stop()
