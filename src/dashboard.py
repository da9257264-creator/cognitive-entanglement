import os
import sys
import yaml
import cv2
from flask import Flask, render_template, Response
from flask_socketio import SocketIO, emit

# Include workspace root directory into sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.drone_controller import DroneController
from src.gesture_detector import GestureDetector
from src.eye_tracker import EyeTracker
from src.body_tracker import BodyTracker
from src.voice_controller import VoiceController
from src.fusion_engine import FusionEngine

app = Flask(__name__, template_folder='../templates')
socketio = SocketIO(app, cors_allowed_origins="*")

# Load configuration parameters
config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "config/config.yaml")
with open(config_path, "r") as f:
    config = yaml.safe_load(f)

# Instantiate core platform components
drone = DroneController(mode=config["system"]["mode"])
gesture_det = GestureDetector(
    min_confidence=config["gestures"]["min_tracking_confidence"],
    cross_threshold=config["gestures"]["cross_hand_distance_threshold"]
)
eye_det = EyeTracker(
    ear_thresh=config["eyes"]["ear_threshold"],
    dot_max=config["eyes"]["dot_max_duration"],
    dash_max=config["eyes"]["dash_max_duration"],
    char_space=config["eyes"]["char_spacing_time"]
)
body_det = BodyTracker(
    follow_dist=config["body"]["follow_distance_factor"],
    tolerance=config["body"]["follow_tolerance"],
    motion_thresh=config["body"]["motion_threshold"]
)
voice_det = VoiceController()
fusion = FusionEngine(drone, config)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('telemetry_update')
def handle_web_telemetry(data):
    client_gesture = data.get("gesture", "NONE")
    client_morse = data.get("morse_cmd", "NONE")
    client_voice = data.get("voice_cmd", "NONE")
    client_body_state = data.get("body_state", "STOPPED")
    client_body_vectors = data.get("body_vectors", {"vx": 0.0, "vy": 0.0, "vz": 0.0, "vyaw": 0.0})
    
    # Extract voice modifiers
    voice_speed = data.get("voice_speed_scale", 1.0)
    voice_height = data.get("voice_height_offset", 0.0)
    
    # Extract GPS tracking coordinates
    gps_coords = data.get("gps_data", None)
    
    # Extract Draw-to-Fly coordinates
    draw_coords = data.get("draw_coords", None)
    
    # Extract Formation and Tracking Target directives
    formation_cmd = data.get("formation_cmd", None)
    tracking_target_cmd = data.get("tracking_target_cmd", None)
    
    # Send directly to central fusion logic
    fusion.update(
        client_gesture, 
        client_morse, 
        client_voice, 
        client_body_vectors, 
        client_body_state,
        gps_data=gps_coords,
        voice_speed_scale=voice_speed,
        voice_height_offset=voice_height,
        draw_coords=draw_coords,
        formation_cmd=formation_cmd,
        tracking_target_cmd=tracking_target_cmd
    )
    
    # Get interactive setup wizard status
    wizard_status = fusion.wizard.get_current_instructions() if hasattr(fusion, 'wizard') else None
    
    leader_telemetry = drone.get_telemetry()
    swarm_telemetry = fusion.swarm.get_swarm_telemetry()
    
    # Override visual leader battery level with decaying simulated onboard battery
    leader_telemetry["battery"] = int(fusion.onboard_battery)
    
    emit('drone_telemetry', {
        "leader": leader_telemetry,
        "swarm": swarm_telemetry,
        "security_authorized": fusion.authorized,
        "current_state": fusion.system_state,
        "delivery_stage": fusion.delivery_stage,
        "wizard": wizard_status,
        "active_formation": fusion.swarm.formation_type,
        "tracking_target": fusion.object_tracker.target_class
    })

@socketio.on('webrtc_signaling')
def handle_webrtc_signaling(data):
    """Broadcasts WebRTC offers, answers, and ICE candidates between Phone A and Phone B."""
    emit('webrtc_signaling', data, broadcast=True, include_self=False)

def run_local_cv():
    """Fallback native pipeline using local webcam."""
    cap = cv2.VideoCapture(0)
    drone.connect()
    voice_det.start_listening()
    
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret: break
        
        # Process visual frames
        frame, gesture = gesture_det.process_frame(frame)
        frame, morse_cmd = eye_det.process_frame(frame)
        frame, body_vectors, body_state = body_det.process_frame(frame)
        voice_cmd, voice_audio = voice_det.get_latest_command()
        
        # Central processing
        fusion.update(gesture, morse_cmd, voice_cmd, body_vectors, body_state, frame=frame, audio_raw=voice_audio)
        
        # Render visual logs
        fusion.security.draw_security_hud(frame)
        fusion.emotion.draw_emotion_hud(frame)
        
        cv2.imshow("Cognitive Entanglement - Local Vision Pipeline", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
    cap.release()
    cv2.destroyAllWindows()
    voice_det.stop_listening()

if __name__ == '__main__':
    drone.connect()
    socketio.run(app, host='0.0.0.0', port=5000, debug=False, allow_unsafe_werkzeug=True)
