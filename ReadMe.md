# 🖐️ Hand Gesture Volume Control System

A **Computer Vision based desktop application** that allows users to control their **system volume using hand gestures** detected through a webcam.

The system uses **MediaPipe Hand Tracking**, **OpenCV**, and a **Tkinter dashboard UI** to detect gestures, measure finger distance, and map it to real-time system volume.

---

# 🎯 Project Overview

This application captures live video from the webcam and detects hand landmarks using **MediaPipe**.
The distance between the **thumb tip** and **index finger tip** is calculated and mapped to **system volume levels (0–100%)**.

The interface provides **real-time feedback**, including:

* Gesture classification
* Current volume level
* Distance measurement
* Detection performance metrics
* Visual volume control indicator
* Distance-to-volume mapping graph

---

# 🚀 Features

### 🎥 Real-Time Hand Detection

* Detects up to **4 hands simultaneously**
* Tracks **21 hand landmarks**
* Displays hand skeleton on the video feed

### ✋ Gesture Recognition

Based on the distance between thumb and index finger:

| Distance      | Gesture   | Action        |
| ------------- | --------- | ------------- |
| `< 40 px`     | Closed    | Mute Volume   |
| `40 – 120 px` | Pinch     | Medium Volume |
| `> 120 px`    | Open Hand | High Volume   |

---

### 🔊 System Volume Control

* Maps finger distance to **0–100% system volume**
* Uses **Pycaw** to control Windows master audio
* Smooth volume transitions

---

### 📊 Performance Monitoring

The UI displays real-time system performance:

* Detection FPS
* Latency
* Frame processing time
* Camera resolution
* Number of detected hands

---

### 📈 Distance–Volume Graph

Live visualization of:

* Finger distance
* Corresponding volume level
* Real-time mapping indicator

---

### 🎛 Adjustable Detection Parameters

Users can tune the model behavior directly from the UI:

| Parameter            | Range     |
| -------------------- | --------- |
| Detection Confidence | 0.1 – 1.0 |
| Tracking Confidence  | 0.1 – 1.0 |
| Max Hands            | 1 – 4     |

Changing parameters **reloads the MediaPipe model dynamically**.

---

### 🎨 Interactive UI Dashboard

The Tkinter interface contains:

* Detection Status Panel
* Current Volume Display
* Detection Parameters
* Detection Info
* Distance Measurement
* Distance–Volume Graph
* Gesture State Indicators
* Live Camera Preview

---

# 🧠 System Workflow

```
Webcam Input
      │
      ▼
MediaPipe Hand Detection
      │
      ▼
Landmark Extraction (21 points)
      │
      ▼
Thumb–Index Distance Calculation
      │
      ▼
Gesture Classification
      │
      ▼
Volume Mapping (0–100%)
      │
      ▼
System Volume Adjustment (Pycaw)
      │
      ▼
UI Feedback + Graph Update
```

---

# 🛠 Technologies Used

| Technology | Purpose                   |
| ---------- | ------------------------- |
| Python     | Core Programming Language |
| OpenCV     | Webcam processing         |
| MediaPipe  | Hand landmark detection   |
| Tkinter    | GUI interface             |
| Pycaw      | Windows volume control    |
| NumPy      | Mathematical operations   |
| Pillow     | Image processing          |
| Matplotlib | Graph visualization       |

---

# 📦 Installation

Install required dependencies:

```bash
pip install opencv-python mediapipe numpy pillow pycaw comtypes matplotlib
```

⚠ **Note:**
Pycaw works only on **Windows operating systems**.

---

# ▶️ How to Run

Clone or download the project and run:

```bash
python Milestone04.py
```

---

# 🕹 Usage Instructions

1. Launch the application
2. Click **Start Camera**
3. Show your hand in front of the webcam
4. Adjust volume using thumb and index finger distance
5. Click **Stop Camera** to stop detection
6. Click **Exit** to close the application

---

# 📊 Interface Overview

### Live Gesture Control

Displays:

* Hand landmarks
* Gesture distance line
* Volume bar indicator

### Detection Status

Shows:

* Camera status
* Current gesture
* Number of detected hands
* Detection FPS
* Latency

### Current Volume

Large visual display showing current system volume percentage.

### Distance Measurement

Displays the real-time distance between thumb and index finger.

### Distance to Volume Mapping

Graph showing the relationship between finger distance and system volume.

---

# 🧪 Testing

Testing was performed through **real-time gesture interaction using webcam input**.

| Test Case      | Expected Result  |
| -------------- | ---------------- |
| Start Camera   | Webcam activates |
| Closed Gesture | Volume set to 0% |
| Pinch Gesture  | Volume ≈ 50%     |
| Open Hand      | Volume ≈ 100%    |
| No Hand        | Gesture = None   |

---

# ⚠ Notes

* Ensure **good lighting conditions** for better detection accuracy.
* Keep the hand **clearly visible to the camera**.
* Recommended distance from camera: **30–70 cm**.
* System performance may affect FPS.

Thank you!