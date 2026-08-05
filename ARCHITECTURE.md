# Hierarchical Flight Control Architecture: Cognitive Entanglement 🛸📐

This document outlines the **aerospace-grade, distributed hierarchical flight control stack** of **Cognitive Entanglement**. As an aeronautical system, its control loops are segmented into distinct levels of authority to guarantee maximum **aerodynamic stability, memory-safety, sub-millisecond precision, and rapid reflex reactions**.

---

## 📐 Multi-Language Aerospace Flight Stack

```text
+--------------------------------------------------------------------------+
|                 OUTER-LOOP: HUMAN-MACHINE INTERFACE                      |
|  - Language: TypeScript & JavaScript (WebGL / MediaPipe JS)              |
|  - Frequency: 60Hz (GPU-Accelerated in-browser)                          |
|  - Role: High-dimensional visual landmark tracking, WebRTC streaming.     |
+------------------------------------+-------------------------------------+
                                     | (Low-Latency WebRTC Data Channel)
                                     v
+--------------------------------------------------------------------------+
|                  LOW-LATENCY WEBRTC SIGNALING CORE                       |
|  - Language: Go (Golang)                                                 |
|  - Frequency: Sub-millisecond packet routing via Goroutines              |
|  - Role: Mutex-locked concurrent WebRTC peer-to-peer handshake packets.  |
+------------------------------------+-------------------------------------+
                                     | (Cellular Internet - TCP/UDP)
                                     v
+--------------------------------------------------------------------------+
|                MID-LOOP: COGNITIVE GUIDANCE ENGINE                       |
|  - Language: Python (Onboard Companion / Phone A)                        |
|  - Frequency: 50Hz - 100Hz                                               |
|  - Role: Path planning, 3D blockade avoidance, EMA smoothing, biometrics. |
+------------------------------------+-------------------------------------+
                                     | (Local Shared Memory / IPC)
                                     v
+--------------------------------------------------------------------------+
|              SAFETY-CRITICAL MONITORING: ONBOARD WATCHDOG                |
|  - Language: Rust                                                        |
|  - Frequency: 10Hz polling with sub-microsecond latency                  |
|  - Role: High-integrity thread safe failsafe, monitoring, heartbeats.     |
+------------------------------------+-------------------------------------+
                                     | (USB Host API Client Interface)
                                     v
+--------------------------------------------------------------------------+
|               ONBOARD PLUG-AND-PLAY USB-SERIAL GATEWAY                   |
|  - Language: C# (C-Sharp / Xamarin / Mono Spec)                          |
|  - Frequency: 1000Hz Bidirectional packet bridging                       |
|  - Role: Direct USB-OTG serial-port-to-WebSocket MAVLink transceiver.    |
+------------------------------------+-------------------------------------+
                                     | (921,600 bps UART Serial - MAVLink)
                                     v
+--------------------------------------------------------------------------+
|               NEON SIMD ACCELERATION: DIRECT REGISTER MATH               |
|  - Language: ARM Assembly (AArch64 / ASM)                                |
|  - Frequency: Sub-microsecond instantaneous operations                   |
|  - Role: Parallel 4-lane single instruction vector scaling.               |
+------------------------------------+-------------------------------------+
                                     | (Hardware register mapping)
                                     v
+--------------------------------------------------------------------------+
|                 INNER-LOOP: ATTITUDE STABILIZATION                       |
|  - Language: C++ (PX4 / ArduPilot Autopilot Firmware)                    |
|  - Frequency: 1000Hz (Real-Time Autopilot)                               |
|  - Role: EKF3 state estimation, PID rate loops, ESC motor mixing.        |
+------------------------------------+-------------------------------------+
                                     | (Direct Register Address Maps)
                                     v
+--------------------------------------------------------------------------+
|               BARE-METAL: DRIVERS & PERIPHERAL BUSES                     |
|  - Language: C (Bare-Metal Microcontroller Drivers)                      |
|  - Frequency: Asynchronous / Interrupt-Driven                            |
|  - Role: Direct DMA transfers, I2C/SPI sensor readouts (LiDAR, IMU).     |
+--------------------------------------------------------------------------+
```

---

## 🛠️ Level-by-Level Engineering Breakdown

### 1. Bare-Metal: Direct Sensor Communication (C)
*   **Platform**: Microcontroller registers (STM32 / H7 series processors).
*   **Frequency**: Asynchronous / Interrupt-Driven.
*   **Aerodynamic Role**: This bare-metal layer is written in **C** to interface directly with physical sensors (IMU, barometer, magnetometers, LiDAR altitude rangefinders) over SPI/I2C. It minimizes CPU load using direct memory access (DMA) transfers.

### 2. Inner-Loop: Attitude Stabilization & Motor Mixing (C++)
*   **Platform**: Flight Controller board (e.g., Pixhawk 6C / Cube Orange) running PX4 or ArduPilot.
*   **Frequency**: **1000Hz (1ms execution cycles)**.
*   **Aerodynamic Role**: This **C++** layer is responsible for the physics of flight. It runs a high-frequency **Extended Kalman Filter (EKF3)** to estimate roll, pitch, yaw, and altitude, and runs the nested PID attitude rate controllers.

### 3. Hardware-Accelerated Math: NEON SIMD Scaling (Assembly)
*   **Platform**: Onboard Phone A (64-bit ARM Cortex-A CPU).
*   **Frequency**: Sub-microsecond execution.
*   **Aerodynamic Role**: Written in **ARM Assembly (ASM)**, this component leverages **AArch64 NEON SIMD** technology. It loads and multiplies 4 single-precision float coordinates in parallel inside the CPU registers in a single instruction cycle. This completely eliminates mathematical latency during high-frequency coordinate frame projections, maximizing reflex speeds.

### 4. Onboard USB-to-Serial Transceiver (C#)
*   **Platform**: Onboard Phone A (via Android USB Host APIs / Xamarin Background Service).
*   **Frequency**: **1000Hz Bidirectional**.
*   **Aerodynamic Role**: Written in **C#** to utilize native Android USB Host ports. When you plug the flight controller into Phone A via a USB-OTG cable, this C# background service instantly bridges low-level serial packets directly to your local companion server with sub-millisecond packet latency, making connection **plug-and-play**.

### 5. Safety-Critical: Onboard Heartbeat Watchdog (Rust)
*   **Platform**: Onboard Companion Computer / "Drone Brain" (Phone A).
*   **Frequency**: 10Hz polling with sub-microsecond fail-response.
*   **Aerodynamic Role**: Written in **Rust** to guarantee compile-time memory safety, zero-cost abstractions, and data-race-free multithreading. It acts as an isolated, high-integrity safety watchdog that monitors the health of the Python cognitive loop and the WebRTC communication channels.

### 6. Mid-Loop: Cognitive Guidance & Safety Overrides (Python)
*   **Platform**: Onboard Companion Computer (**Phone A** mounted on the frame).
*   **Frequency**: **50Hz - 100Hz**.
*   **Aerodynamic Role**: Written in **Python**, this layer acts as the tactical navigator. It computes where the drone *should* fly safely based on your commands:
    *   **3D Blockade Sensing**: Segments camera frames into Front, Up, and Down sectors to detect obstacle proximity. If a blockade is sensed, it overrides guidance to climb or dive.
    *   **Exponential Moving Average (EMA) Filtering**: Smooths out high-frequency skeletal tremor noise from the tracking camera before sending target locations, preventing violent flight movements.

### 7. Low-Latency WebRTC Signaling Core (Go)
*   **Platform**: Cloud Web server / Telemetry Broker.
*   **Frequency**: Sub-millisecond routing.
*   **Aerodynamic Role**: Written in **Go (Golang)** to utilize high-concurrency **Goroutines** and mutex-locked maps. It routes your hand tracking, eye Morse blinks, and voice commands between Phone B and Phone A over 5G networks with zero lag, ensuring instantaneous reflexes.

### 8. Outer-Loop: Human-Machine Interface & Computer Vision (TypeScript & JavaScript)
*   **Platform**: Ground Station Browser / Pilot Phone (**Phone B**).
*   **Frequency**: **60Hz (GPU-Accelerated)**.
*   **Aerodynamic Role**: This layer handles high-dimensional, heavy-lifting computer vision. By running **MediaPipe JS** directly inside Phone B's web browser, we utilize the mobile GPU to map facial meshes, hands, and body skeletons at a fluid 60fps without burdening the onboard flight companion (Phone A).
*   **Type Safety**: Written in **TypeScript** (`src/telemetry_types.ts`) to enforce strict type schemas, interfaces, and packet contracts for our WebSockets, preventing memory leaks or unexpected data types from crashing the client.

### 9. DevOps & Build Automation (Bash, Docker, & GNU Make)
*   **Platform**: Local development terminal or onboard Companion operating system.
*   **Role**: Written in **Bash** (`deploy.sh`), **Dockerfile**, and **Makefile** to fully automate environmental configuration, containerized microservice deployments, package dependency updates, and compile your high-integrity Rust, C++, and Go binaries with a single terminal command: `make`.

---

## 🛡️ Multi-Tiered Failsafe Matrix

To prevent flyaways and guarantee aircraft survivability, the system implements hierarchical hardware/software failsafes:

1.  **Level 1 Failsafe (Autopilot / C++)**: If the serial cable between Phone A and the Pixhawk is severed, the Pixhawk immediately triggers an onboard **RC Failsafe**, automatically entering a stationary GPS hold or executing an RTL (Return-to-Land).
2.  **Level 2 Failsafe (Companion / Rust & Python)**: If the WebRTC connection or video call between Phone B and Phone A drops for over **1.5 seconds**, Phone A's Rust watchdog engine triggers a **Loss-of-Signal (LOS) Failsafe**, sending a MAVLink command to immediately hover or execute a controlled vertical descent.
3.  **Level 3 Failsafe (Ground / TypeScript & JS)**: If the browser's tab loses focus or frames stop rendering, the client automatically halts coordinate transmission, forcing Phone A to enter failsafe mode.
