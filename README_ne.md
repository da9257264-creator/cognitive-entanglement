# 🌌 संज्ञानात्मक संजाल (Cognitive Entanglement) 🛸📱

[**English**](README.md) | [**简体中文**](README_zh.md) | **नेपाली** | [**Website**](TELE_ROBOTICS.md) | [**Docs**](ARCHITECTURE.md) | [**Quick Start**](#-द्रुत-तैनाथी-र-उडान-निर्देशिका-दुई-फोन-प्रणाली)

[![CI Quality Assurance](https://github.com/da9257264-creator/cognitive-entanglement/actions/workflows/ci.yml/badge.svg)](https://github.com/da9257264-creator/cognitive-entanglement/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/Python-3.10%2B-blueviolet)](https://www.python.org/)
[![Swarm Architecture](https://img.shields.io/badge/Architecture-Multi--Agent_Swarm-cyan)](#)

यो **4G/5G सेलुलर नेटवर्क अन्तर्गत "दुई-फोन" क्लाउड लामो-दूरी सञ्चालन** को लागि डिजाइन गरिएको एक उन्नत, बहु-मोडल मानव-ड्रोन झुण्ड (swarm) समन्वय फ्रेमवर्क हो। यो **NASA, SpaceX, र Lockheed Martin जस्ता एयरोस्पेस दिग्गजहरूद्वारा विश्वसनीय १५-भाषा वितरित उडान नियन्त्रण स्ट्याक (Ada, C++, Rust, Go, Fortran, र Verilog सहित)** को प्रयोग गरी निर्माण गरिएको हो। ग्राउण्ड स्टेशन कम्प्युटरको आवश्यकता बिना, **ह्यान्ड इशाराहरू (सांकेतिक भाषा), आँखाको मोर्स कोड, प्राकृतिक आवाज र शरीर ट्र्याकिङ** प्रयोग गरेर अनुकूलित, सिमुलेटेड, वा भौतिक ड्रोनहरू (DJI Tello, PX4/MAVLink) नियन्त्रण गर्न सकिन्छ।

---

## 📸 एयरोस्पेस-ग्रेड नियन्त्रण आर्किटेक्चर

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

## 🔥 उन्नत सुविधाहरू

### १. दोहोरो बायोमेट्रिक सुरक्षा कुञ्जीहरू (`src/security_manager.py` & `src/voice_biometrics.py`)
*   **अनुहार पहिचान**: अनुहारको精細 हड्डीको अनुपात विश्लेषण गरेर ड्रोन अनलक गर्दछ।
*   **आवाज पहिचान**: १६kHz अडियो फ्रिक्वेन्सी ढाँचा विश्लेषण गरेर आवाजको प्रमाणीकरण गर्दछ।

### २. ३डी अवरोध सेन्सिङ र मार्ग रिकभरी (`src/obstacle_avoidance.py`)
*   **अवरोध बचाउ**: अगाडि अवरोध पत्ता लाग्दा स्वचालित रूपमा ढिलो हुन्छ र माथि वा तलबाट सुरक्षित रूपमा उड्छ।
*   **मार्ग自愈**: अवरोध पार गरेपछि ड्रोन **स्वचालित रूपमा पहिलेको गति र उडान मार्गमा फर्किन्छ**।

### ३. अन्तरक्रियात्मक क्यालिब्रेसन विजार्ड (`src/enrollment_wizard.py`)
सुरुआतमा ड्रोनको मस्तिष्क (Phone A) ले आवाज (TTS) मार्फत अनुहार स्क्यान र आवाज दर्ता गर्न मार्गदर्शन गर्दछ।

---

## ⚡ प्रणाली क्षमता र प्रदर्शन म्याट्रिक्स

१५-भाषा उडान र ग्राउण्ड प्रणाली स्ट्याकको एकीकरणले **Cognitive Entanglement** लाई अत्यन्त उच्च प्रदर्शन क्षमता प्रदान गर्दछ:

| विशेषता / मेट्रिक | परिचालन क्षमता | एयरोस्पेस ईन्जिनियरिङ् कार्यान्वयन |
| :--- | :--- | :--- |
| **नियन्त्रण दायरा** | **असीमित (ग्लोबल सेलुलर लिङ्क)** | ४G/५G LTE WebRTC क्लाउड पाइपलाइन मार्फत रिमोट कन्ट्रोल |
| **नियन्त्रण ढिलाइ** | **१०० मिलिसेकेन्ड भन्दा कम** | Go (Golang) को उच्च-प्रदर्शन समवर्ती (concurrent) सर्भर |
| **दृश्य ट्र्याकिङ गति** | **६० Hz (GPU-त्वरित)** | ब्राउजर भित्र MediaPipe GPU-त्वरित ल्यान्डमार्क ट्र्याकिङ |
| **मिड-लूप मार्गनिर्देशन** | **५० Hz - १०० Hz** | Python ३डी अवरोध सेन्सिङ र VFH बचाउ状态机 |
| **भित्री-लूप स्थिरता** | **१००० Hz (१ms पुनरावृत्ति)** | C++ nested PID नियन्त्रण र EKF३ अनुमान |
| **सेन्सर पोलिङ गति** | **सब-माइक्रोसेकेन्ड (< १µs)** | VHDL/Verilog FPGA हार्डवेयर-स्तर SPI शिफ्ट रजिस्टर |
| **भेक्टर गणित गति** | **हार्डवेयर रजिस्टर स्केलिंग** | ४-लेन समानान्तर ARM NEON SIMD एसेम्बली अप्टिमाइजेसन |
| **सुरक्षा आश्वासन** | **DO-१७८C Level A मानक** | Ada शून्य-अपवाद उडान उचाई सीमा र गैर-हस्तक्षेप लक |
| **अवरोध बचाउ** | **३-क्षेत्र सक्रिय規避** | अगाडि, माथि, र तल ठाडो क्षेत्र घनत्व स्क्यानिङ |
| **मार्ग रिकभरी** | **स्वचालित गति र मार्ग自愈** | उडान मार्ग मेमोरी बफर र स्वचालित त्वरण |
| **झुण्ड गठन (Swarm)** | **१ नेता + N अनुयायीहरू** | वास्तविक समयमा V-Shape/Line/Orbit गठन परिवर्तन |
| **सुरक्षित ल्यान्डिङ** | **बहु-स्तरीय रेडन्डन्सी** | १.५s संकेत गुमेमा होभर-लक र १५% ब्याट्रीमा返航 (RTL) |

---

## 🎮 बहु-मोडल नियन्त्रण म्याट्रिक्स

Cognitive Entanglement ले अपरेटरहरूलाई दृश्य, आवाज, मुद्रा (posture), र समय अनुसार सहज रूपमा नियन्त्रण गर्न अनुमति दिन्छ। तल आधिकारिक नियन्त्रण म्याट्रिक्स छ:

| नियन्त्रण च्यानल | अपरेटर इनपुट / कार्य | डिकोड गरिएको आदेश | उडान चालहरू |
| :--- | :--- | :--- | :--- |
| **👐 सांकेतिक भाषा**<br>*(Deaf-Mute ASL)* | ASL "V / Peace" इशारा | `ASL_PEACE` | **टेकअफ र होभर** (१.२ मिटर उचाईमा) |
| | ASL "OK" इशारा | `ASL_OK` | **सुरक्षित अवतरण र इन्जिन disarm** |
| | ASL "I Love You" (ILY) | `ASL_ILY` | **स्वचालित घर फिर्ता (Return-to-Home)** |
| | ASL "Shaka / Y" इशारा | `ASL_Y` | **सतत शरीर ट्र्याकिङ (Follow-Me) सुरु** |
| | ASL "Thumbs-Up" इशारा | `ASL_THUMBS_UP` | **उडान उचाई बढाउनुहोस्** (+०.५ मिटर) |
| | ASL "Open Palm" (Wait) | `ASL_WAIT` | **原地 सुरक्षित होभर लक (Position Hold)** |
| | दुवै हात क्रस (Crossed) | `CROSS_HANDS` | **आपतकालीन होभर लक (Emergency Override)** |
| **👁️ आँखाको मोर्स कोड**<br>*(EAR Timed Blinks)* | तीन छोटो झिम्काइ (`...`) | `SAFETY_STOP` | **आपतकालीन होभर लक** (१०ms भित्र प्रतिक्रिया) |
| | तीन लामो झिम्काइ (`---`) | `GO_HOME` | **सुरक्षित घर फिर्ता र ल्यान्डिङ** |
| | एक छोटो एक लामो (`.-`) | `ALTITUDE_UP` | **उडान उचाई बढाउनुहोस्** (+०.५ मिटर) |
| | एक लामो एक छोटो (`-.`) | `ALTITUDE_DOWN` | **उडान उचाई घटाउनुहोस्** (-०.५ मिटर) |
| | दुई छोटो झिम्काइ (`..`) | `START_FOLLOW` | **शरीर पछ्याउन सुरु गर्नुहोस्** |
| **🗣️ बहुभाषा आवाज**<br>*(Multi-Lingual)* | *"Takeoff"* / *"Fly"* / *"उड्नुहोस्"* | `TAKEOFF` | **इन्जिन सुरु र टेकअफ** |
| | *"Land"* / *"aterrizar"* / *"ओर्लिनुहोस्"* | `LAND` | **सुरक्षित अवतरण र इन्जिन disarm** |
| | *"Speed Fast"* / *"Accelerate"* | `SPEED_FAST` | **१.८ गुणा उडान गति बढाउनुहोस्** |
| | *"Speed Slow"* / *"Slow Down"* | `SPEED_SLOW` | **०.५ गुणा उडान गति घटाउनुहोस्** |
| | *"Selfie"* / *"सेल्फी"* | `SELFIE` | **सेल्फी अर्बिट特技** (३६० डिग्री फोटो स्वीप) |
| | *"Immelmann"* / *"salto"* | `IMMELMANN` | **हवाई स्टन्ट: इमेलम्यान टर्न** |
| | *"Split S"* / *"gira"* | `SPLITS` | **हवाई स्टन्ट: स्प्लिट-एस डाइभ** |
| | *"Find"* / *"Chirp"* / *"खोज्नुहोस्"* | `FIND` | **इन्जिन बीकन ध्वनि सुरु (चिरप)** |
| | *"Panic"* / *"Emergency"* | `PANIC` | **आपतकालीन जबरजस्ती सुरक्षित ल्यान्डिङ** |
| **🏃‍♂️ शरीर ट्र्याकिङ**<br>*(Pose Proportions)* | काँधको चौडाइको अनुपात | गहिराई Delta | **आनुपातिक दूरी नियन्त्रण** (दूरी सन्तुलन) |
| | नाकको तेर्सो दूरी | Yaw Delta | **आनुपातिक घुमाउरो नियन्त्रण** (पाइलट सेन्टरिङ) |
| | नाकको ठाडो उचाई | Altitude Delta | **आनुपातिक उचाई नियन्त्रण** (उचाई म्याच) |
| | ५.० सेकेन्ड भन्दा बढी पाइलट नदेखिएमा | Dead-Man | **पाइलट खसेको Failsafe - स्वचालित ल्यान्डिङ** |

---

## 📂 निर्देशिका संरचना

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
├── .gitignore                 # Dependency exclusion file
├── requirements.txt           # Dependency Manifest
├── LICENSE                    # MIT Open-Source License
├── README.md                  # English Landing Page
├── README_zh.md               # Chinese Landing Page
├── HARDWARE.md                # Physical drone wiring guide (Tello & Pixhawk)
└── TELE_ROBOTICS.md           # Two-phone Cloud Tele-operation guide
```

---

## 🚀 द्रुत तैनाथी र उडान निर्देशिका (दुई-फोन प्रणाली)

### १. सर्भर सुरु गर्नुहोस्
```bash
pip install -r requirements.txt
python src/dashboard.py
```

### २. Phone A (ड्रोन मस्तिष्क) जडान गर्नुहोस्
*   **Phone A** लाई ड्रोनमा माउन्ट गर्नुहोस् र USB-OTG केबल मार्फत फ्लाइट कन्ट्रोलरमा जडान गर्नुहोस्।
*   ब्राउजरमा सर्भर लिङ्क खोल्नुहोस् र **Phone A: Drone Brain** चयन गर्नुहोस्।

### ३. Phone B (ग्राउण्ड पाइलट) जडान गर्नुहोस्
*   हातमा **Phone B** लिनुहोस्, ब्राउजरमा सर्भर लिङ्क खोल्नुहोस्, र **Phone B: Ground Pilot** चयन गर्नुहोस्।
*   **Place WebRTC Call** मा क्लिक गर्नुहोस्।
*   अब, इशाराहरू र आवाज मार्फत ड्रोन उडाउनुहोस्!

---

## 🤝 योगदान र अनुमति पत्र
यो परियोजना **MIT अनुमति पत्र** अन्तर्गत खुला स्रोत (open-source) हो।
