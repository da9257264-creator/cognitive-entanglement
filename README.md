# Cognitive Entanglement 🛸📱

[![CI Quality Assurance](https://github.com/<your-username>/cognitive-entanglement/actions/workflows/ci.yml/badge.svg)](https://github.com/<your-username>/cognitive-entanglement/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/Python-3.10%2B-blueviolet)](https://www.python.org/)
[![Swarm Architecture](https://img.shields.io/badge/Architecture-Multi--Agent_Swarm-cyan)](#)

An advanced, multi-modal human-drone swarm orchestration framework designed **exclusively for 2-Phone Cloud Tele-operation over 4G/5G LTE**. Control simulated or physical drones (DJI Tello, PX4/MAVLink) over infinite distances using **Sign Language, Eye-Morse Code, Natural Voice Speech, and Proportional Body-Tracking**.

---

## 📸 Architectural Pipeline

```text
                               +----------------------------------------+
                               |     Webcam Video & Voice Mic Input     |
                               +-------------------+--------------------+
                                                   |
                   +-------------------------------+---------------------------------+
                   |                               |                                 |
+------------------v---------+   +-----------------v---------+             +---------v---------+
|    MediaPipe FaceMesh      |   |     MediaPipe Hands       |             |   Local/Browser   |
+------------------+---------+   +-----------------+---------+             |   Vocal Capture   |
                   |                               |                       +---------+---------+
    +--------------+------------+                  +--------------+                  |
    |                           |                                 |                  |
+---v-------------+     +-------v---------+               +-------v---------+        |
|Biometric Facial |     |Emotion Analysis |               | Gesture Control |        |
|  Authorization  |     | (Wobble on Smile|               |& Crossed Wrists |        v
+---+-------------+     |  Retreat on Fear|               +-------+---------+  +-----+-----------+
    |                   +-------+---------+                       |            | Voice Command   |
    |                           |                                 |            | Decoder (STT)   |
    +---------------------------+----------------+----------------+            +-----+-----------+
                                                 |                                   |
                                                 v                                   v
                               +-----------------+-----------------------------------+
                               |       Multi-Modal Priority & Safety Fusion          |
                               |    (Dual-Factor Facial & Voice Biometric Lock)      |
                               +-------------------------+---------------------------+
                                                         |
                                        +----------------+----------------+
                                        | (Leader Velocity Vectors)       |
                                        v                                 v
                          +-------------+-------------+     +-------------+-------------+
                          |   Obstacle Avoidance      |     |  Multi-Drone Swarm Engine |
                          |   Radar (Dodge Vector)    |     | (Triangle/V-Shape Offsets)|
                          +-------------+-------------+     +-------------+-------------+
                                        |                                 |
                                        +----------------+----------------+
                                                         |
                                                         v
                                      +------------------+------------------+
                                      |   Unified Hardware/Simulator API    |
                                      |  (Tello Flips, PX4, or Three.js)    |
                                      +-------------------------------------+
```

---

## 🔥 Cutting-Edge Cognitive Features

### 1. Dual-Factor Biometric Keys (`src/security_manager.py` & `src/voice_biometrics.py`)
Safety is fortified by double-factor biometric verification:
*   **Facial Biometrics**: Captures high-dimensional facial proportions (chin depth relative to eyebrow spacing) to verify identity before arming.
*   **Speaker Recognition (Voice Footprints)**: Analyzes raw 16kHz audio streams to compute unique vocal pitch distributions and spectral centroids. Commands spoken by unregistered voices are blocked, rendering the drone immune to ambient talk or hijacks.

### 2. Physical & Simulated Aerial Tricks Engine (`src/tricks_engine.py`)
Trigger high-intensity maneuvers using either voice commands or eye blinks:
*   **Acrobatic Flips (`front_flip`, `back_flip`, `left_flip`, `right_flip`)**: Transmitted directly via DJI Tello SDK, or modeled visually on the 3D dashboard.
*   **Inward Orbit Carousel**: Performs a 360-degree orbit around you, banking and yawing continuously to keep the nose locked on your position.
*   **Tornado Spiral Takeoff**: A high-speed ascending yaw spin that lifts the entire swarm upward.
*   **Eagle Sine-Glide**: Undulates up and down in a smooth, sinusoidal flight path while gliding forward.
*   **Victory Wobble Dance**: An excited left-to-right wobble sequence showing active drone feedback.

### 3. Interactive Vocal Calibration Wizard (`src/enrollment_wizard.py`)
Perfect for beginners! On startup, the drone's brain (Phone A) vocally guides you step-by-step through a friendly 4-stage setup to scan your face, enroll your voice footprint, and verify your ASL hand tracking before any flight maneuvers are unlocked.

### 4. Interactive Draw-To-Fly curves
Simple navigation for anyone! Directly draw any flight curve with your finger on **Phone B's** touchscreen. The interface translates your drawing into local coordinate vectors and commands the drone to fly that path automatically.

### 5. 3D Sector Blockade Sensing & Path Recovery (`src/obstacle_avoidance.py`)
Our visual collision radar segments the video frame's lower hemisphere into 3 discrete hazard sectors. If a physical obstacle encroaches a sector, it produces artificial "repulsion vectors" that combine with your steering vectors, enabling the drone to seamlessly glide around objects.

### 6. Swarm Formation Layer (`src/swarm_controller.py`)
Coordinate multiple drones simultaneously! The operator controls the "Leader" drone directly, while the Swarm engine dynamically propagates safe flocking offsets (cohesion, alignment) to any number of virtual "Follower" drones, flying them in formation.

---

## 📂 Repository Layout

```text
cognitive-entanglement/
├── .github/
│   └── workflows/
│       └── ci.yml             # GitHub Actions Quality Gate Pipeline
├── config/
│   └── config.yaml            # Thresholds, safety constraints, emotion scales
├── src/
│   ├── __init__.py
│   ├── drone_controller.py    # Unified API (Simulator, Tello SDK, PX4 MAVLink)
│   ├── gesture_detector.py    # MediaPipe Hands (standard ASL mute signs & crossed wrists)
│   ├── eye_tracker.py         # MediaPipe FaceMesh EAR Morse Code Decoder
│   ├── body_tracker.py        # MediaPipe Pose tracking (follower vectors)
│   ├── voice_controller.py    # Speech-to-Text natural language parser
│   ├── voice_biometrics.py    # Speaker voiceprint verification matching
│   ├── tricks_engine.py       # Aerial acrobatics coordinator (flips, spins, orbits)
│   ├── security_manager.py    # FaceMesh Biometric Verification lock
│   ├── emotion_engine.py      # FaceMesh expression analysis & actions
│   ├── swarm_controller.py    # Follower formation calculator (leader-centric)
│   ├── obstacle_avoidance.py  # VFH sector density visual safety scanner
│   ├── enrollment_wizard.py   # Interactive vocal calibration setup guide
│   ├── fusion_engine.py       # Core Multi-modal state machine coordinator
│   └── dashboard.py           # Flask-SocketIO Web Dashboard backend
├── templates/
│   └── index.html             # UI Dashboard (3D Swarm Simulator, WebRTC Call HUD)
├── tests/
│   └── test_ai_drone.py       # Comprehensive unit test suite (100% passing!)
├── requirements.txt           # Dependency Manifest
├── LICENSE                    # MIT Open-Source License
├── README.md                  # Showcase Landing Page
├── HARDWARE.md                # Physical drone wiring guide (Tello & Pixhawk)
└── TELE_ROBOTICS.md           # Two-phone Cloud Tele-operation guide
```

---

## 🛠️ Execution & Deployment (The 2-Phone System)

### 1. Launch Cloud Web Dashboard Server
Install dependencies and launch the backend server:
```bash
pip install -r requirements.txt
python src/dashboard.py
```

### 2. Connect Your Onboard Phone A (The Drone Brain)
*   Mount **Phone A** onto your physical drone frame.
*   Connect **Phone A** to the flight controller (Pixhawk telemetry or USB) via a USB-OTG cable.
*   Open the dashboard on **Phone A**'s web browser and click **Phone A: Drone Brain**.

### 3. Connect Your Ground Phone B (The Ground Pilot)
*   Hold **Phone B** in your hand on the ground (or place it on a tripod).
*   Open the dashboard on **Phone B**'s web browser and click **Phone B: Ground Pilot**.
*   Click **Place WebRTC Call** on **Phone B** to establish an instant FPV call to **Phone A**.
*   **The system is now live!** Stand in front of **Phone B**'s camera. **Phone A (onboard the drone)** will watch your live stream, process all your ASL signs, voice commands, and eye blinks locally on the drone, and execute maneuvers in real-time over unlimited distance!

---

## 🤝 Contribution & Support
We love open source! Open an Issue or submit a Pull Request to contribute to the future of Human-Robot Collaboration.

Distributed under the MIT License. See `LICENSE` for more details.
