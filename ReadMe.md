# 🖐️ Hand Gesture Volume Controller

Control your **system volume** in real-time using **hand gestures** powered by **MediaPipe**, **OpenCV**, and **Tkinter GUI**.

This application detects your hand via webcam, measures the distance between your **thumb and index finger**, classifies gestures, and adjusts the system volume accordingly.

---

## 🚀 Features

* 🎥 Real-time webcam hand tracking
* ✋ Gesture classification:

  * **Closed** → Mute
  * **Pinch** → Medium volume
  * **Open Hand** → High volume
* 🔊 Direct system volume control (via Pycaw)
* 📊 Live detection stats:

  * FPS
  * Latency
  * Resolution
  * Frame time
* 🎛 Adjustable:

  * Detection confidence
  * Tracking confidence
  * Max number of hands
* 📏 Real-time pixel distance measurement
* 🎨 Clean scrollable Tkinter interface

---

## 🧠 How It Works

1. MediaPipe detects 21 hand landmarks.
2. The distance between:

   * Thumb tip (Landmark 4)
   * Index tip (Landmark 8)
3. Distance is mapped to:

   * Gesture state
   * Volume percentage (0–100%)
4. Pycaw updates system master volume.

---

## 🖼️ Gesture Logic

| Distance (px) | Gesture   | Action        |
| ------------- | --------- | ------------- |
| < 40 px       | Closed    | Mute (0%)     |
| 40 – 120 px   | Pinch     | Medium Volume |
| > 120 px      | Open Hand | High Volume   |

---

## 📦 Requirements

Install dependencies:

```bash
pip install opencv-python mediapipe numpy pillow pycaw comtypes
```

> ⚠️ Windows only (Pycaw works with Windows audio endpoint)

---

## ▶️ How to Run

```bash
python your_script_name.py
```

Then:

1. Click **Start Camera**
2. Show your hand in front of the webcam
3. Control volume using thumb & index finger distance
4. Click **Stop Camera** when finished

---

## 🛠 Technologies Used

* Python 3.x
* OpenCV
* MediaPipe
* Tkinter
* Pycaw
* NumPy
* Pillow

---

## 📊 Interface Sections

* Detection Status
* Detection Parameters
* Detection Info
* Distance Measurement
* Gesture States
* Real-time Video Feed

---

## 🎯 Controls

| Button       | Function                     |
| ------------ | ---------------------------- |
| Start Camera | Activates webcam & detection |
| Stop Camera  | Stops webcam                 |
| Exit         | Closes application           |

---

## ⚙ Adjustable Parameters

* **Detection Confidence** (0.1 – 1.0)
* **Tracking Confidence** (0.1 – 1.0)
* **Max Hands** (1 – 4)

Changing parameters reloads the MediaPipe model automatically.

---

## 📌 Notes

* Good lighting improves detection accuracy.
* Keep your hand clearly visible.
* Recommended distance from camera: 30–70 cm.
* FPS depends on your system performance.

---

## 🔮 Future Improvements (Optional Ideas)

* Add smoothing to volume changes
* Add gesture-based brightness control
* Add left/right hand distinction
* Cross-platform audio support
* Add dark/light mode toggle

---

Thank you!