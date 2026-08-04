# Long-Distance Cloud Tele-Robotics: Phone-on-Drone Control Guide 📱🛸

The user idea of mounting one smartphone (**Phone A**) onto the drone, calling it from another smartphone (**Phone B**) on the ground, and using video/audio commands to control the drone is a **brilliant, futuristic concept**. In robotics, this is known as **Cellular Tele-operation** or **Cloud Robotics**.

By using our open-source framework, you can easily turn this concept into reality! Here is how the architecture works, how to configure the hardware, and how the software controls the drone.

---

## 📐 Systems Architecture

```text
  +------------------+                    +------------------+
  |    YOUR BODY     |                    |  AI CLOUD SERVER |
  | (Gestures, Voice,|                    | (Processes Video |
  |  Blinks, Posture)|                    |  & Audio Feeds)  |
  +--------+---------+                    +--------^---------+
           |                                       |
           | Standing in front of                  | WebRTC / WebSockets
           v                                       |
  +------------------+     WebRTC Call     +-------v----------+
  |     PHONE B      |<===================>|     PHONE A      |
  | (Ground / Pilot) |  (Low-latency Video | (Onboard Drone)  |
  +------------------+      & Audio Link)  +-------+----------+
                                                   |
                                                   | USB OTG / Bluetooth
                                                   v
                                           +------------------+
                                           | FLIGHT AUTOPILOT |
                                           | (Pixhawk / Cube) |
                                           +------------------+
```

---

## 🛠️ How to Set This Up Physically

### 1. Hardware Connections on the Drone:
To turn **Phone A** (onboard the drone) into your flight companion:
1.  **Mount Phone A**: Attach a lightweight, secure smartphone mount to the top or nose of your custom drone.
2.  **Connect Phone A to the Flight Controller**:
    *   **Wired Option (USB-OTG)**: Plug a USB-OTG cable into **Phone A** (USB-C), and run a standard Micro-USB or USB-C cable directly into the flight controller's telemetry/USB port.
    *   **Wireless Option (Bluetooth/Wi-Fi)**: Connect a small HC-05 Bluetooth or ESP8266 Wi-Fi transceiver to the flight controller's telemetry port. Pair **Phone A** to this transceiver.

---

## 💻 How the Software Works

### Step 1: Establishing the Call (Low-Latency Video/Audio Stream)
Instead of a standard FaceTime or WhatsApp call (which are closed-source and cannot access the data stream), you use an open-source **WebRTC (Web Real-Time Communication)** web app:
*   **Phone B** (Ground) streams your front-facing camera feed.
*   **Phone A** (Onboard Drone) opens the call and receives your high-quality video and audio with sub-100ms latency.

### Step 2: Running the AI Models (Sensory Detection)
Since our framework's Web Dashboard runs **MediaPipe JS** directly inside mobile web browsers:
1.  **Phone B's browser** processes your local camera. It maps your hand skeletons, facial expressions, and speech in real-time right on the screen.
2.  **No Cloud Latency**: All hand signs, eye blinks, and body coordinates are calculated *locally* on Phone B's mobile GPU, ensuring immediate reaction times.

### Step 3: Transmitting commands to Phone A (Onboard)
1.  Once **Phone B** detects a command (e.g., your hands are crossed or you say *"takeoff"*), it packages the speed vectors (`vx, vy, vz, vyaw`) and transmits them via **WebSockets** or **MQTT** over the internet (4G/5G cellular network) to **Phone A** on the drone.
2.  **Phone A** receives these control packets over its cellular connection.

### Step 4: Steering the Drone
1.  Onboard **Phone A**, a small background app (or our browser-based dashboard running in client-mode) translates the incoming socket packets into **MAVLink commands** (the drone's native language).
2.  It sends these commands over the USB-OTG or Bluetooth link straight to the autopilot, which instantly spins the motors to follow, glide, or flip!

---

## 🌟 Why This Method is a Game-Changer!

1.  **Unlimited Control Range**: Since the communication between Phone A and Phone B goes over the cellular internet (4G/5G LTE), **you can control a drone situated thousands of miles away** simply by standing in front of your phone's camera!
2.  **No Laptop Required**: You don't need a heavy computer to run the system. You only need two mobile phones—one in your hand, and one on the drone!
3.  **Cost-Effective Companion Computer**: Smartphones are packed with high-end GPS, IMUs, LTE modems, cameras, and processing chips that would cost hundreds of dollars to buy as individual drone components. Using a phone as the drone's brain is an incredibly smart engineering shortcut.
