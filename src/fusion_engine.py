import time
import logging
from src.security_manager import SecurityManager
from src.emotion_engine import EmotionEngine
from src.swarm_controller import SwarmController
from src.obstacle_avoidance import ObstacleAvoidance
from src.voice_biometrics import VoiceBiometrics
from src.tricks_engine import TricksEngine
from src.enrollment_wizard import EnrollmentWizard
from src.object_tracker import ObjectTracker
from src.audio_dsp_filter import AudioDspFilter
from src.wind_compensator import WindCompensator

class FusionEngine:
    def __init__(self, drone_controller, config):
        self.drone = drone_controller
        self.config = config
        
        self.system_state = "IDLE" 
        self.delivery_stage = "INIT"
        self.handoff_timer = None
        
        # Instantiate advanced subsystems under the "Cognitive Entanglement" name
        self.security = SecurityManager(config)
        self.emotion = EmotionEngine(config)
        self.swarm = SwarmController(swarm_size=config["system"]["swarm_size"])
        self.avoidance = ObstacleAvoidance(config)
        self.voice_bio = VoiceBiometrics(config)
        self.tricks = TricksEngine(self.drone)
        self.wizard = EnrollmentWizard()
        self.object_tracker = ObjectTracker()
        
        # New advanced aerospace modules
        self.dsp_filter = AudioDspFilter()
        self.wind_compensator = WindCompensator()
        
        self.authorized = not config["security"]["biometrics_enabled"]
        self.voice_authorized = not config["security"]["voice_biometrics_enabled"]
        
        # Virtual Geofence boundary
        self.geofence_horizontal_max = 12.0 
        self.geofence_altitude_max = 3.5     
        
        # Draw-to-Fly coordinate tracking queue
        self.draw_flight_queue = []
        self.draw_queue_idx = 0
        
        # Multi-phone tracking coordinates
        self.tracked_phone_gps = {"lat": 0.0, "lon": 0.0, "alt": 0.0}
        
        # Low-pass filter smoothing registers (prevents jerky motions!)
        self.smooth_vx = 0.0
        self.smooth_vy = 0.0
        self.smooth_vz = 0.0
        self.smooth_vyaw = 0.0
        self.smoothing_factor = config["gestures"].get("cross_hand_distance_threshold", 0.35)
        
        # Fallen-Pilot dead man's registers
        self.last_pilot_detection_time = time.time()
        self.dead_man_timeout = config["body"].get("dead_man_timeout", 5.0)
        
        # Battery state registers
        self.onboard_battery = 100.0
        self.last_battery_decay_time = time.time()
        
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger("CognitiveEntanglement")

        # Map Morse signals to maneuvers
        self.MORSE_TRICKS_MAP = {
            ".--.": "tornado_spin",   # P
            "...-": "victory_wobble",  # V
            "-..-": "orbit_carousel", # X
            ".-..-": "eagle_glide"    # F
        }

    def update(self, gesture, morse_cmd, voice_cmd, body_vectors, body_state, face_landmarks=None, frame=None, audio_raw=None, gps_data=None, voice_speed_scale=1.0, voice_height_offset=0.0, draw_coords=None, formation_cmd=None, tracking_target_cmd=None):
        """
        Main decision-maker of the "Cognitive Entanglement" AI system.
        """
        current_time = time.time()

        # Update pilot tracking activity timestamp for the Dead-man's switch
        if face_landmarks is not None or body_state == "MOVING" or gesture != "NONE":
            self.last_pilot_detection_time = current_time

        # Simulate gradual battery drain
        if current_time - self.last_battery_decay_time > 4.0:
            if self.drone.is_flying:
                self.onboard_battery -= 1.0
                self.last_battery_decay_time = current_time

        # 1. Low-Battery Auto-RTL Failsafe
        if self.drone.is_flying and self.onboard_battery <= 15.0:
            self.logger.error("BATTERY CRITICAL (<= 15%)! Self-Healing Failsafe triggered. Autonomous Return-to-Home activated.")
            self.system_state = "RETURNING"
            self._execute_home_run()
            return

        # 2. Dynamic Swarm Formations
        if formation_cmd:
            self.swarm.set_formation(formation_cmd)
        elif voice_cmd in ["FORMATION_V", "FORMATION_LINE", "FORMATION_ORBIT"]:
            form_map = {
                "FORMATION_V": "V-SHAPE",
                "FORMATION_LINE": "LINE",
                "FORMATION_ORBIT": "ORBIT"
            }
            self.swarm.set_formation(form_map[voice_cmd])

        # 3. Audio DSP Prop-Noise Band-Stop Filtering
        if audio_raw:
            audio_raw = self.dsp_filter.denoise_audio_chunk(audio_raw)

        # 4. Voice-Guided Active Object Tracking
        if tracking_target_cmd:
            if tracking_target_cmd == "CANCEL":
                self.object_tracker.cancel_tracking()
            else:
                self.object_tracker.set_target(tracking_target_cmd)
        elif voice_cmd in ["TRACK_PERSON", "TRACK_BICYCLE", "TRACK_CAT", "TRACK_DOG", "TRACK_BALL", "TRACK_BACKPACK", "CANCEL_TRACK"]:
            if voice_cmd == "CANCEL_TRACK":
                self.object_tracker.cancel_tracking()
            else:
                target_class = voice_cmd.replace("TRACK_", "").lower()
                self.object_tracker.set_target(target_class)

        # 5. Interactive Enrollment Wizard (Easy setup)
        if self.wizard.current_step != "READY" and self.config["security"]["biometrics_enabled"]:
            if self.wizard.current_step == "WELCOME" and (gesture != "NONE" or voice_cmd != "NONE"):
                self.wizard.advance_step("START")
            elif self.wizard.current_step == "FACE_SCAN" and face_landmarks is not None:
                is_authorized_face = self.security.authorize_operator(face_landmarks)
                if is_authorized_face:
                    self.authorized = True
                    self.wizard.advance_step("FACE_MATCHED")
            elif self.wizard.current_step == "VOICE_SCAN" and voice_cmd == "SECURE_AUTH":
                self.voice_authorized = True
                self.wizard.advance_step("VOICE_MATCHED")
            elif self.wizard.current_step == "GESTURE_CHECK" and gesture == "ASL_PEACE":
                self.wizard.advance_step("GESTURE_MATCHED")
                self.system_state = "IDLE"
            
            # Keep drone locked and stopped during setup
            self.drone.stop()
            return

        # ----------------------------------------------------
        # 6. Emergency Panics & Wait Overrides
        # ----------------------------------------------------
        is_emergency = (voice_cmd in ["PANIC", "KILL", "CRASH", "EMERGENCY"]) or (morse_cmd == "SAFETY_STOP") or (gesture == "CROSS_HANDS") or (voice_cmd == "STOP")
        if is_emergency:
            self.logger.warn("COGNITIVE ENTANGLEMENT: Emergency Kill Switch active! Landing immediately.")
            self.drone.land()
            self.system_state = "IDLE"
            self.draw_flight_queue = []
            return

        is_wait = (gesture == "ASL_WAIT") or (voice_cmd == "WAIT") or (morse_cmd == "SAFETY_STOP")
        if is_wait:
            self.logger.info("COGNITIVE ENTANGLEMENT: Wait / Position Hold active. Freezing translations.")
            self.drone.stop()
            self.system_state = "STOPPED"
            self._update_swarm()
            return

        # ----------------------------------------------------
        # 7. Fallen-Pilot Recovery (Dead-Man's Switch)
        # ----------------------------------------------------
        if self.drone.is_flying and (current_time - self.last_pilot_detection_time > self.dead_man_timeout):
            self.logger.error(f"Fallen-Pilot Failsafe! No operator detected. Landing drone safely.")
            self.drone.land()
            self.system_state = "IDLE"
            self._update_swarm()
            return

        # ----------------------------------------------------
        # 8. Draw-To-Fly curves pathing
        # ----------------------------------------------------
        if draw_coords:
            self.draw_flight_queue = draw_coords
            self.draw_queue_idx = 0
            self.system_state = "DRAW_FLY"
            self.logger.info(f"Loaded Draw-to-Fly path: {len(draw_coords)} nodes.")

        if self.system_state == "DRAW_FLY" and len(self.draw_flight_queue) > 0:
            if self.draw_queue_idx < len(self.draw_flight_queue):
                target_wp = self.draw_flight_queue[self.draw_queue_idx]
                self.drone.go_to(target_wp["x"], target_wp["y"], target_wp["z"])
                self.draw_queue_idx += 1
                time.sleep(0.5)
            else:
                self.logger.info("Draw-to-Fly completed.")
                self.drone.stop()
                self.system_state = "MANUAL"
            self._update_swarm()
            return

        # ----------------------------------------------------
        # 9. Multi-Phone GPS Tracking
        # ----------------------------------------------------
        if gps_data:
            self.tracked_phone_gps = gps_data
            if self.system_state == "GPS_FOLLOW":
                vx_gps = gps_data.get("dx", 0.0) * 0.5
                vy_gps = gps_data.get("dy", 0.0) * 0.5
                self.drone.set_velocities(vx_gps, vy_gps, 0.0, 0.0)
                self._update_swarm()
                return

        # ----------------------------------------------------
        # 10. Expression-Based Behavioral Modulators
        # ----------------------------------------------------
        safety_scale = 1.0
        if face_landmarks:
            emotion, safety_scale = self.emotion.analyze_mood(face_landmarks)
            if emotion == "HAPPY" and self.system_state in ["MANUAL", "FOLLOW"]:
                self.logger.info("Pilot smile registered. Initiating victory wobble!")
                self.tricks.execute_trick("victory_wobble")

        # ----------------------------------------------------
        # 11. Advanced Aerial Tricks (including Selfie & Finder)
        # ----------------------------------------------------
        if morse_cmd in self.MORSE_TRICKS_MAP:
            self.tricks.execute_trick(self.MORSE_TRICKS_MAP[morse_cmd])
            return

        if voice_cmd in ["FRONT_FLIP", "BACK_FLIP", "LEFT_FLIP", "RIGHT_FLIP", "TORNADO", "DANCE", "GLIDE", "ORBIT", "SELFIE", "FIND", "IMMELMANN", "SPLITS", "BARRELROLL", "CHANDELLE", "ORBIT_SAT", "ROOM_SCAN"]:
            trick_map = {
                "FRONT_FLIP": "front_flip",
                "BACK_FLIP": "back_flip",
                "LEFT_FLIP": "left_flip",
                "RIGHT_FLIP": "right_flip",
                "TORNADO": "tornado_spin",
                "DANCE": "victory_wobble",
                "GLIDE": "eagle_glide",
                "ORBIT": "orbit_carousel",
                "SELFIE": "selfie_orbit",
                "FIND": "beacon_chirp",
                "IMMELMANN": "immelmann_turn",
                "SPLITS": "split_s",
                "BARRELROLL": "barrel_roll",
                "CHANDELLE": "chandelle",
                "ORBIT_SAT": "space_station_orbit",
                "ROOM_SCAN": "room_scan"
            }
            self.tricks.execute_trick(trick_map[voice_cmd])
            return

        # ----------------------------------------------------
        # 12. Basic Controls & Deaf-Mute Signs
        # ----------------------------------------------------
        is_takeoff = (voice_cmd == "TAKEOFF") or (gesture == "ASL_PEACE") or (gesture == "POINTING_UP" and self.system_state == "IDLE")
        is_land = (voice_cmd == "LAND") or (gesture == "ASL_OK") or (gesture == "FIST")
        is_follow = (voice_cmd == "START_FOLLOW") or (gesture == "ASL_Y") or (morse_cmd == "START_FOLLOW")
        is_home = (voice_cmd == "GO_HOME") or (gesture == "ASL_ILY") or (morse_cmd == "GO_HOME")

        if is_takeoff:
            self.drone.takeoff()
            self.system_state = "MANUAL"
            self._update_swarm()
            return
            
        if is_land:
            self.drone.land()
            self.system_state = "IDLE"
            self._update_swarm()
            return

        if is_follow:
            self.system_state = "FOLLOW"
            self.logger.info("Following engaged.")

        if is_home:
            self.system_state = "RETURNING"
            self._execute_home_run()
            return

        if gesture == "ASL_THUMBS_UP":
            self.drone.set_velocities(0, 0, 0.4, 0)
            time.sleep(1.0)
            self.drone.stop()

        # ----------------------------------------------------
        # 13. Active Translation Loop with Onboard ActiveTrack
        # ----------------------------------------------------
        if self.system_state in ["FOLLOW", "MANUAL"]:
            body_vectors["vz"] += voice_height_offset

            # ActiveTrack Override: If active, target coordinates are computed by Object Tracker instead of human pose!
            if self.object_tracker.is_tracking_target:
                frame_out, track_vectors = self.object_tracker.track_object_in_frame(frame)
                body_vectors["vx"] = track_vectors["vx"]
                body_vectors["vyaw"] = track_vectors["vyaw"]
                body_state = "MOVING"

            if body_state == "MOVING" or (body_vectors["vx"] != 0 or body_vectors["vy"] != 0 or body_vectors["vz"] != 0 or body_vectors["vyaw"] != 0):
                
                # Active 3D blockade sensing
                block_data = {"front": 0.0, "up": 0.0, "down": 0.0}
                if frame is not None:
                    block_data = self.avoidance.sense_blockades(frame)
                
                # 🚑 Predictive Crash Avoidance (Kinematic Time-To-Collision evaluation):
                # If approaching a front blockade too fast, trigger immediate emergency braking!
                if block_data["front"] > 0.4 and body_vectors["vx"] > 0.2:
                    current_velocity = body_vectors["vx"]
                    proximity_distance = (1.0 - block_data["front"]) * 2.0 # simulated proximity distance in meters
                    time_to_collision = proximity_distance / (current_velocity + 1e-6)
                    
                    if time_to_collision < 0.8: # Under 0.8 seconds to crash
                        self.logger.error(f"[SAFETY SHIELD]: Predictive Crash Alert! TTC: {time_to_collision:.2f}s. Activating Emergency Brake.")
                        body_vectors["vx"] = -0.4 # Force rapid reverse deceleration!
                        body_vectors["vz"] = 0.3  # Gain height immediately!
                
                safe_vectors = self.avoidance.compute_safe_vectors(block_data, body_vectors)
                
                # Apply speed factors
                target_vx = safe_vectors["vx"] * safety_scale * voice_speed_scale
                target_vy = safe_vectors["vy"] * voice_speed_scale
                target_vz = safe_vectors["vz"]
                target_vyaw = safe_vectors["vyaw"]
                
                # 🌪️ Active Wind Gust ADRC Compensation:
                # Modulates commanded vectors using estimated physical displacement drift
                simulated_imu_drift = {"dx": target_vx * 0.9, "dy": target_vy * 0.9} # Simulate minor outdoor wind drag
                safe_vectors_adrc = self.wind_compensator.estimate_and_compensate(
                    {"vx": target_vx, "vy": target_vy, "vz": target_vz},
                    simulated_imu_drift
                )
                target_vx = safe_vectors_adrc["vx"]
                target_vy = safe_vectors_adrc["vy"]
                
                # 🛡️ Virtual Geofence Check
                telemetry = self.drone.get_telemetry()
                cur_x = telemetry["position"]["x"]
                cur_y = telemetry["position"]["y"]
                cur_z = telemetry["position"]["z"]

                if (cur_x**2 + cur_y**2) > self.geofence_horizontal_max**2:
                    target_vx = -0.3 if cur_x > 0 else 0.3
                    target_vy = -0.3 if cur_y > 0 else 0.3

                if cur_z > self.geofence_altitude_max:
                    target_vz = -0.4

                # 🎛️ EMA smoothing
                self.smooth_vx = (self.smoothing_factor * target_vx) + ((1 - self.smoothing_factor) * self.smooth_vx)
                self.smooth_vy = (self.smoothing_factor * target_vy) + ((1 - self.smoothing_factor) * self.smooth_vy)
                self.smooth_vz = (self.smoothing_factor * target_vz) + ((1 - self.smoothing_factor) * self.smooth_vz)
                self.smooth_vyaw = (self.smoothing_factor * target_vyaw) + ((1 - self.smoothing_factor) * self.smooth_vyaw)

                self.drone.set_velocities(
                    self.smooth_vx,
                    self.smooth_vy,
                    self.smooth_vz,
                    self.smooth_vyaw
                )
            else:
                self.drone.stop()

        elif self.system_state == "DELIVERY":
            self._handle_delivery_logic(gesture, voice_cmd, body_vectors, safety_scale)
            
        self._update_swarm()

    def _handle_delivery_logic(self, gesture, voice, vectors, safety_scale):
        if self.delivery_stage == "INIT":
            self.delivery_stage = "APPROACHING"
            
        elif self.delivery_stage == "APPROACHING":
            scaled_vx = vectors["vx"] * (1.0 / safety_scale)
            self.drone.set_velocities(scaled_vx, vectors["vy"], vectors["vz"], vectors["vyaw"])
            
            if abs(scaled_vx) < 0.05:
                self.drone.stop()
                self.delivery_stage = "HOVERING_FOR_HANDOFF"
                
        elif self.delivery_stage == "HOVERING_FOR_HANDOFF":
            if voice == "HANDOFF_DONE" or gesture == "OPEN_PALM":
                self.delivery_stage = "COUNTDOWN_TO_RETURN"
                self.handoff_timer = time.time()
                
        elif self.delivery_stage == "COUNTDOWN_TO_RETURN":
            if time.time() - self.handoff_timer > 3.0:
                self.system_state = "RETURNING"
                self.delivery_stage = "INIT"
                self._execute_home_run()

    def _execute_home_run(self):
        self.drone.set_velocities(0, 0, 0.4, 0)
        time.sleep(1.5)
        self.drone.go_to(
            self.config["delivery"]["home_position"][0],
            self.config["delivery"]["home_position"][1],
            self.config["delivery"]["home_position"][2]
        )
        time.sleep(3)
        self.drone.land()
        self.system_state = "IDLE"

    def _update_swarm(self):
        telemetry = self.drone.get_telemetry()
        self.swarm.update_swarm_positions(
            telemetry["position"],
            telemetry["yaw"],
            telemetry["flight_mode"]
        )
