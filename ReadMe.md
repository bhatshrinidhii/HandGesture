# ✋ Hand Gesture Volume Controller (MediaPipe + OpenCV + Tkinter)

A real-time computer vision application that controls system volume using hand gestures detected through a webcam.
Built using **Python, MediaPipe, OpenCV, and Tkinter GUI**.

This project demonstrates practical usage of computer vision for Human-Computer Interaction (HCI).

---

## 📌 Features

* 🎥 Live webcam feed inside GUI
* 🖐️ Detects multiple hands (configurable)
* 📍 21 hand landmarks tracking
* 🔊 Volume control using pinch gesture (thumb + index)
* 🔇 Automatic mute when fist detected
* 📊 Real-time dashboard:

  * Hands detected
  * Detection FPS
  * Latency (ms)
  * Model status
* 🎚 Adjustable detection parameters:

  * Detection confidence (%)
  * Tracking confidence (%)
  * Maximum hands (1-4)
* 📉 Visual volume bar display

---

## 🧠 Gestures

| Gesture                | Action          |
| ---------------------- | --------------- |
| 🤏 Thumb + Index pinch | Adjust volume   |
| ✊ Closed fist         | Mute volume     |
| Open hand              | Active tracking |

---

## 🛠 Technologies Used

* Python 3.10
* OpenCV
* MediaPipe Hands
* Tkinter GUI
* NumPy
* Pillow

---

## 📂 Project Structure

```
HandGesture/
|__ camera_test.py
│── gesture_ui.py
│── README.md
```

---

## ⚙️ Installation

### 1️⃣ Clone the repository

```
git clone https://github.com/bhatdhrinidhii/HandGestureVolumeControl.git
cd HandGestureVolumeControl
```

### 2️⃣ Create virtual environment

```
python -m venv venv
venv\Scripts\activate   # Windows
```

### 3️⃣ Install dependencies

pip install opencv-python mediapipe==0.10.9 numpy pillow


## ▶️ Run the Application

```
python gesture_ui.py
```

---

## 🧩 How It Works

1. Webcam captures frames
2. MediaPipe detects 21 hand landmarks
3. Distance between thumb tip (ID 4) and index tip (ID 8) is calculated
4. Distance mapped to volume percentage
5. GUI updates volume bar & stats in real-time

---

## 📊 Detection Parameters

| Parameter            | Purpose                               |
| -------------------- | ------------------------------------- |
| Detection Confidence | Probability required to detect a hand |
| Tracking Confidence  | Stability of landmark tracking        |
| Max Hands            | Maximum simultaneous hands detectable |

---

## 🎯 Learning Outcomes

* Real-time computer vision processing
* Human-computer interaction design
* GUI integration with CV pipelines
* MediaPipe landmark interpretation
* Performance optimization (FPS & latency monitoring)

---

Thank You!
