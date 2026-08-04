# Physical Drone Hardware Integration Guide 🛠️🛸

This guide explains how to connect your physical drone hardware (DJI Tello or custom PX4/ArduPilot quadcopters) directly to the **Cognitive Entanglement 2-Phone Cloud Tele-operation System**. 

In this setup, **Phone A (mounted on the drone)** acts as the local "companion computer" and "autonomous brain", while **Phone B (in your hand)** acts as the remote pilot webcam.

---

## Option A: DJI Tello (Zero Hardware Modifications)
The DJI Tello is a ready-to-fly toy drone that contains an onboard Wi-Fi access point and developer SDK.

### Connections:
1.  Mount **Phone A** securely to the top of the Tello frame using a lightweight smartphone clip.
2.  Turn on the Tello drone.
3.  Connect **Phone A**'s Wi-Fi directly to the Tello's hotspot (e.g., `TELLO-XXXXXX`).
4.  Configure `mode: "tello"` inside `config/config.yaml`.
5.  On **Phone A**, open the Web Dashboard and select **Phone A: Drone Brain**. The onboard phone will now route MAVLink and UDP SDK commands straight into the Tello's receiver over Wi-Fi!

---

## Option B: Custom DIY Drone (Advanced PX4 or ArduPilot)
To control a custom-built quadcopter, you must connect **Phone A** directly to the drone's flight controller (autopilot).

### 1. Required Onboard Hardware:
Mount these physical components directly on your custom drone frame:

| Component | Purpose | Recommended Hardware |
| :--- | :--- | :--- |
| **Flight Autopilot** | Handles physics, motor mixing, and stabilization. | Pixhawk 6C, Cube Orange+, or Kakute H7. |
| **Drone Brain Phone (Phone A)** | Processes WebRTC incoming video frames, runs MediaPipe, and translates signs/speech to MAVLink. | Any smartphone with a fast GPU and USB-C port. |
| **USB-OTG Adapter** | Wired interface from Phone A to the Flight Controller. | USB-C to USB-A (OTG) adapter. |
| **Onboard USB Cable** | Connects the OTG adapter to the flight controller. | Micro-USB or USB-C cable. |

### 2. Physical Wiring Diagram:
```text
 +--------------------------------------------------------------------------------+
 |                             PHYSICAL DRONE FRAME                               |
 |                                                                                |
 |  +-----------------------+   USB-OTG Cable    +-----------------------------+  |
 |  |   FLIGHT CONTROLLER   |<------------------>|     DRONE BRAIN PHONE       |  |
 |  |  (Pixhawk / Cube / H7)|   Wired serial     |         (Phone A)           |  |
 |  |                       |                    |  (Runs MediaPipe & Sockets) |  |
 |  +-----------+-----------+                    +--------------+--------------+  |
 |              |                                               |                 |
 |              v                                               v                 |
 |       To Motors & ESCs                              4G/5G Cellular Antenna     |
 +--------------------------------------------------------------+-----------------+
                                                                |
                                                                | WebRTC Cloud Call
                                                                v
                                                 +--------------+--------------+
                                                 |      GROUND PILOT PHONE     |
                                                 |          (Phone B)          |
                                                 +-----------------------------+
```

---

## 3. Autopilot Parameter Configuration:
You must configure your flight controller to receive high-speed serial telemetry from **Phone A**:

1.  Connect your flight controller to your laptop and open **QGroundControl** or **Mission Planner**.
2.  Go to **Parameters** and configure your main USB/Serial telemetry port:
    *   `SERIAL2_PROTOCOL` (or port protocol equivalent) ➔ Set to `2` (MAVLink 2, the communication language).
    *   `SERIAL2_BAUD` ➔ Set to `921600` (Enables high-speed 921,600 bps serial to eliminate lag).
3.  For safety, configure your **Failsafe Actions**:
    *   Set `FS_GCS_ENABLE` to `1` (Ensures the drone automatically returns to home and lands if it loses connection with the pilot).

---

## 4. How to Launch and Fly:

1.  Turn on your drone.
2.  Connect **Phone A** (onboard the drone) to the flight controller via the USB-OTG cable.
3.  Open the Web Dashboard on **Phone A**'s browser, and click **Phone A: Drone Brain**.
4.  Open the Web Dashboard on **Phone B**'s browser (in your hand), and click **Phone B: Ground Pilot**.
5.  Click **Place WebRTC Call** on Phone B to establish a live FPV video/audio link.
6.  **The system is now live!** Stand in front of Phone B's camera. Your video feed is streamed over the network to **Phone A**, which runs MediaPipe to analyze your gestures, ASL signs, and voice commands onboard the aircraft, piloting your drone over unlimited distance!
