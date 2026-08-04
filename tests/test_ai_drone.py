import unittest
import numpy as np
import yaml
import os
import sys

# Add root folder to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.drone_controller import DroneController
from src.gesture_detector import GestureDetector
from src.eye_tracker import EyeTracker
from src.body_tracker import BodyTracker
from src.voice_controller import VoiceController
from src.security_manager import SecurityManager
from src.emotion_engine import EmotionEngine
from src.swarm_controller import SwarmController
from src.obstacle_avoidance import ObstacleAvoidance
from src.voice_biometrics import VoiceBiometrics
from src.fusion_engine import FusionEngine

class TestCognitiveEntanglement(unittest.TestCase):
    def setUp(self):
        # Fallback configuration representing default production settings
        self.config = {
            "system": {
                "mode": "simulator",
                "debug": True,
                "swarm_size": 3
            },
            "security": {
                "biometrics_enabled": False,
                "voice_biometrics_enabled": False,
                "voice_signature_threshold": 0.15,
                "auth_facial_ratio_threshold": 0.05,
                "authorized_user_profile": {
                    "eye_to_mouth_ratio": 1.15,
                    "jaw_to_eyebrow_ratio": 0.85
                }
            },
            "emotions": {
                "facial_expression_tracking": True,
                "safety_distance_scale_fear": 1.8,
                "smile_action": "victory_roll"
            },
            "eyes": {
                "ear_threshold": 0.22,
                "dot_max_duration": 0.4,
                "dash_max_duration": 1.5,
                "char_spacing_time": 1.8,
                "word_spacing_time": 3.5
            },
            "gestures": {
                "min_tracking_confidence": 0.7,
                "cross_hand_distance_threshold": 0.08
            },
            "body": {
                "follow_distance_factor": 0.15,
                "follow_tolerance": 0.02,
                "motion_threshold": 0.03,
                "motion_window_size": 10
            },
            "avoidance": {
                "enabled": True,
                "sensor_field_of_view": 90,
                "safety_distance": 1.0,
                "reaction_gain": 1.5
            },
            "delivery": {
                "safe_approach_distance": 0.20,
                "handoff_timeout": 5.0,
                "home_position": [0.0, 0.0, 1.2]
            }
        }
        self.drone = DroneController(mode="simulator")
        self.drone.connect()
        self.drone.takeoff() # Prepare drone for simulated flight

    def test_drone_controller_simulator(self):
        """Verifies simulated flight vectors and coordinate updates."""
        self.assertTrue(self.drone.is_flying)
        self.drone.set_velocities(0.5, -0.2, 0.1, 0.5)
        telemetry = self.drone.get_telemetry()
        
        # Simulated interpolation should update position
        self.assertNotEqual(telemetry["position"]["x"], 0.0)
        self.assertNotEqual(telemetry["position"]["y"], 0.0)
        self.assertNotEqual(telemetry["position"]["z"], 0.0)
        self.assertNotEqual(telemetry["yaw"], 0.0)

    def test_swarm_formations(self):
        """Verifies follower drones form accurate relative spatial V-formations."""
        swarm = SwarmController(swarm_size=3, separation_dist=1.5)
        leader_pos = {"x": 2.0, "y": 1.0, "z": 1.5}
        leader_yaw = 90.0 # Facing east
        leader_mode = "GUIDED"
        
        swarm.update_swarm_positions(leader_pos, leader_yaw, leader_mode)
        followers = swarm.get_swarm_telemetry()
        
        # Follower 2 (Left-rear flank) and Follower 3 (Right-rear flank)
        self.assertEqual(followers[2]["flight_mode"], "GUIDED")
        self.assertEqual(followers[3]["flight_mode"], "GUIDED")
        
        # The coordinates should not overlap the leader, and must show symmetry
        self.assertNotEqual(followers[2]["position"]["x"], leader_pos["x"])
        self.assertNotEqual(followers[3]["position"]["x"], leader_pos["x"])
        self.assertEqual(followers[2]["position"]["z"], leader_pos["z"])

    def test_voice_biometrics_spectral_extraction(self):
        """Verifies voice acoustic analysis can process raw PCM chunks and create signatures."""
        voice = VoiceBiometrics(self.config)
        
        # Generate dummy 1s mono PCM 16kHz sine wave representation
        sample_rate = 16000
        t = np.linspace(0, 1, sample_rate, endpoint=False)
        audio_sine = np.sin(2 * np.pi * 150 * t) * 32767 # 150Hz tone
        audio_bytes = audio_sine.astype(np.int16).tobytes()
        
        signature = voice._extract_vocal_signature(audio_bytes, sample_rate)
        self.assertIsNotNone(signature)
        self.assertAlmostEqual(signature[0], 150.0, delta=5.0) # Matches fundamental pitch

    def test_obstacle_avoidance_and_path_recovery(self):
        """Verifies 3D blockade sensing triggers auto-height maneuvers and remembers tracking paths."""
        avoid = ObstacleAvoidance(self.config)
        
        # Target path given by tracking tracker (forward at 0.5m/s)
        target_path = {"vx": 0.5, "vy": 0.0, "vz": 0.0, "vyaw": 0.0}
        
        # Sector blockade status showing Front is blocked, but Up is clear
        blockade_data = {"front": 0.8, "up": 0.1, "down": 0.2}
        
        # Evaluate collision vector adjustment
        safe_path = avoid.compute_safe_vectors(blockade_data, target_path)
        
        # Forward speed must decelerate, and altitude must climb to scale blockade
        self.assertLess(safe_path["vx"], 0.5)
        self.assertGreater(safe_path["vz"], 0.0)
        self.assertTrue(avoid.is_bypassing)
        
        # Sensed clear path: front density goes back to zero
        clear_data = {"front": 0.0, "up": 0.0, "down": 0.0}
        recovered_path = avoid.compute_safe_vectors(clear_data, safe_path)
        
        # Original forward speed should be restored completely from trajectory memory
        self.assertEqual(recovered_path["vx"], 0.5)
        self.assertEqual(recovered_path["vz"], 0.0)
        self.assertFalse(avoid.is_bypassing)

if __name__ == '__main__':
    unittest.main()
