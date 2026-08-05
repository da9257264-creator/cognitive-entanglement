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
        """Acrobatic half-loop climb followed by 180-degree roll to recover level opposite flight."""
        self.logger.info("AEROBATICS: Commencing IMMELMANN TURN.")
        # Step 1: Rapid climb half-loop (vz=0.8, vx=0.3)
        self.drone.set_velocities(0.3, 0.0, 0.8, 0.0)
        time.sleep(1.5)
        
        # Step 2: 180-degree roll recovery (roll=1.5, yaw=2.0)
        self.drone.set_velocities(0.0, 1.5, 0.0, 2.0)
        time.sleep(0.8)
        self.drone.stop()

    def _execute_split_s(self):
        """Rolls 180 degrees into inverted flight, then executes descending half-loop."""
        self.logger.info("AEROBATICS: Commencing SPLIT-S tactical dive.")
        # Step 1: Invert roll (roll=1.8)
        self.drone.set_velocities(0.0, 1.8, 0.0, 0.0)
        time.sleep(0.6)
        
        # Step 2: Descending dive half-loop (vz=-0.8, vx=0.4)
        self.drone.set_velocities(0.4, 0.0, -0.8, 0.0)
        time.sleep(1.2)
        self.drone.stop()

    def _execute_barrel_roll(self):
        """Helical 360-degree roll forward gliding maneuver."""
        self.logger.info("AEROBATICS: Commencing BARREL ROLL.")
        start_time = time.time()
        while time.time() - start_time < 2.0:
            elapsed = time.time() - start_time
            # Rotate roll sinusoidally while moving forward
            roll = 1.5 * math.sin(math.pi * elapsed)
            self.drone.set_velocities(0.5, roll, 0.0, 0.0)
            time.sleep(0.1)
        self.drone.stop()

    def _execute_chandelle(self):
        """High-performance climbing turn, gaining altitude while turning 180 degrees."""
        self.logger.info("AEROBATICS: Commencing CHANDELLE climbing turn.")
        self.drone.set_velocities(0.4, 0.0, 0.5, 1.5) # Climb while yawing
        time.sleep(2.0)
        self.drone.stop()
