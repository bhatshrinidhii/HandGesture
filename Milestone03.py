import tkinter as tk
from tkinter import ttk
import cv2
import mediapipe as mp
import numpy as np
import math
import time
from PIL import Image, ImageTk
from pycaw.pycaw import AudioUtilities

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

big_volume_label = None
# Get default speakers endpoint
devices = AudioUtilities.GetSpeakers()

# Get volume interface directly
volume = devices.EndpointVolume

# Get volume range
vol_min, vol_max, _ = volume.GetVolumeRange()

conf_value_label = None
track_value_label = None

distance_value = 0
gesture_state = "None"

closed_label = None
pinch_label = None
open_label = None

# ---------------- MEDIAPIPE ----------------
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = None
prev_time = 0

current_max_hands = 1

def create_hand_model():
    global hands, current_max_hands

    current_max_hands = int(maxhands_slider.get())

    if hands:
        hands.close()   # VERY IMPORTANT (releases old model)

    hands = mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=current_max_hands,
        min_detection_confidence=conf_slider.get(),
        min_tracking_confidence=track_slider.get()
    )

    model_label.config(text=f"Model Loaded ({current_max_hands} hands)", fg="lightgreen")


# ---------------- CAMERA VARIABLES ----------------
cap = None
running = False
volume_percent = 50
gesture_text = "None"

# ---------------- CAMERA LOOP ----------------
def update_frame():
    global volume_percent, gesture_text, prev_time
    global distance_value, gesture_state
    global closed_label, pinch_label, open_label
    global big_volume_label

    # Detect slider change live
    if int(maxhands_slider.get()) != current_max_hands:
        create_hand_model()

    global volume_percent, gesture_text, prev_time

    if not running:
        return

    start = time.time()

    ret, frame = cap.read()
    if not ret:
        return

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    hand_count = 0

    if results.multi_hand_landmarks:
        hand_count = len(results.multi_hand_landmarks)

        for i, hand_landmarks in enumerate(results.multi_hand_landmarks):
            cv2.putText(frame, f'Hand {i+1}', (10, 40 + i*30),
            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)

            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            h, w, _ = frame.shape
            lm_list = []

            for id, lm in enumerate(hand_landmarks.landmark):
                cx, cy = int(lm.x * w), int(lm.y * h)
                lm_list.append((cx, cy))

            fingers = []
            fingers.append(1 if lm_list[4][0] > lm_list[3][0] else 0)

            tips = [8, 12, 16, 20]
            pips = [6, 10, 14, 18]

            for tip, pip in zip(tips, pips):
                fingers.append(1 if lm_list[tip][1] < lm_list[pip][1] else 0)

            total = fingers.count(1)

            if total == 0:
                volume_percent = 0
                gesture_text = "MUTE"
            else:
                distance_value = 0
                gesture_state = "No Hand"
                gesture_text = "No Hand"
                closed_label.config(fg="white")
                pinch_label.config(fg="white")
                open_label.config(fg="white")

                x1, y1 = lm_list[4]
                x2, y2 = lm_list[8]

                # distance in pixels
                length = math.hypot(x2 - x1, y2 - y1)
                distance_value = int(length)

                # midpoint
                cx, cy = (x1 + x2)//2, (y1 + y2)//2

                # draw measurement
                cv2.line(frame, (x1,y1), (x2,y2), (255,0,255), 2)
                cv2.circle(frame, (cx,cy), 6, (0,255,0), cv2.FILLED)
                cv2.putText(frame, f'{distance_value}px', (cx+10,cy-10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 2)

                # ---- Gesture Classification ----
                if length < 40:
                    gesture_state = "Closed"
                elif length < 120:
                    gesture_state = "Pinch"
                else:
                    gesture_state = "Open Hand"

                # Reset all colors
                closed_label.config(fg="white")
                pinch_label.config(fg="white")
                open_label.config(fg="white")

                # Highlight active state
                if gesture_state == "Closed":
                    closed_label.config(fg="red")
                elif gesture_state == "Pinch":
                    pinch_label.config(fg="orange")
                elif gesture_state == "Open Hand":
                    open_label.config(fg="lightgreen")

                gesture_text = gesture_state

                # still control volume
                volume_percent = int(np.interp(length, [20, 200], [0, 100]))

                system_vol = np.interp(volume_percent, [0, 100], [vol_min, vol_max])
                volume.SetMasterVolumeLevel(system_vol, None)
                
                target_volume = np.interp(length, [20, 200], [0, 100])
                volume_percent = int(volume_percent + (target_volume - volume_percent) * 0.2)  # keep last volume

    # -------- INFO PANEL UPDATE --------
    hands_label.config(text=f"Hands: {hand_count}")

    curr_time = time.time()
    fps = int(1 / (curr_time - prev_time)) if prev_time != 0 else 0
    prev_time = curr_time
    fps_label.config(text=f"Detection FPS: {fps}")

    latency = int((time.time() - start) * 1000)
    latency_label.config(text=f"Latency: {latency} ms")

    # ---- Detection Info Update ----
    resolution_label.config(text=f"Resolution: {frame.shape[1]}x{frame.shape[0]}")
    frametime_label.config(text=f"Frame Time: {latency} ms")

    # -------- VOLUME BAR --------
    vol_bar = np.interp(volume_percent, [0, 100], [300, 50])
    cv2.rectangle(frame, (30, 50), (60, 300), (0,255,0), 2)
    cv2.rectangle(frame, (30, int(vol_bar)), (60, 300), (0,255,0), -1)

    cv2.putText(frame, f'{volume_percent}%', (20, 340),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,255), 2)

    # Convert frame → Tkinter
    img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    imgtk = ImageTk.PhotoImage(image=img)

    video_label.imgtk = imgtk
    video_label.configure(image=imgtk)

    volume_label.config(text=f"Volume: {volume_percent}%")
    gesture_label.config(text=f"Gesture: {gesture_text}")

    big_volume_label.config(text=f"{volume_percent}%")
    distance_label.config(text=f"{distance_value} px")
    # state_label.config(text=gesture_state)

    line.set_data([0, 200], [0, 100])
    point.set_data([distance_value], [volume_percent])
    canvas_graph.draw()

    root.after(10, update_frame)

# ---------------- BUTTONS ----------------
def start_camera():
    global cap, running
    if not running:
        cap = cv2.VideoCapture(0)
        running = True
        status_label.config(text="Camera Status : Active", fg="lightgreen")
        create_hand_model()
        update_frame()

def stop_camera():
    global running
    running = False
    if cap:
        cap.release()
    status_label.config(text="Camera Stopped", fg="red")

# ---------------- UI ----------------
def update_conf_label(val):
    global conf_value_label
    percent = int(float(val) * 100)
    if conf_value_label:
        conf_value_label.config(text=f"{percent}%")

def update_track_label(val):
    global track_value_label
    percent = int(float(val) * 100)
    if track_value_label:
        track_value_label.config(text=f"{percent}%")


root = tk.Tk()
root.title("Hand Gesture Volume Controller")
root.geometry("1000x800")
root.configure(bg="#74c2fa")

title = tk.Label(root, text="Hand Detection Interface",
                 font=("Arial", 16, "bold"), bg="#1e1e1e", fg="white")
title.pack(pady=10)

# -------- BUTTONS --------
btn_frame = tk.Frame(root, bg="#74c2fa")
btn_frame.pack(pady=20)

tk.Button(btn_frame, text="Start Camera", bg="#2254f8", command=start_camera, width=15).grid(row=0, column=0, padx=10)
tk.Button(btn_frame, text="Stop Camera", bg="#2254f8", command=stop_camera, width=15).grid(row=0, column=1, padx=10)
tk.Button(btn_frame, text="Exit", bg="#2254f8", command=root.destroy, width=15).grid(row=0, column=2, padx=10)

main_frame = tk.Frame(root, bg="#1e1e1e")
main_frame.pack()

video_label = tk.Label(main_frame, bg="black")
video_label.grid(row=0, column=0, padx=20)

# ---------- SCROLLABLE PANEL ----------
panel_container = tk.Frame(main_frame, bg="#1e1e1e")
panel_container.grid(row=0, column=1, padx=20, sticky="ns")

canvas = tk.Canvas(panel_container, bg="#1e1e1e", width=300, highlightthickness=0)
scrollbar = tk.Scrollbar(panel_container, orient="vertical", command=canvas.yview)

scrollable_frame = tk.Frame(canvas, bg="#1e1e1e")

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

# This becomes your new panel
panel = scrollable_frame

# -----------------------------------------

tk.Label(panel, text="Detection Status", bg="#010779",
         fg="white", font=("Arial", 12, "bold")).pack(pady=(10, 0))
status_label = tk.Label(panel, text="Camera Status: Inactive", bg="#2b2b2b", fg="red", font=("Arial", 12))
status_label.pack(pady=5)

volume_label = tk.Label(panel, text="Volume: 0%", bg="#2b2b2b", fg="white", font=("Arial", 12))
volume_label.pack(pady=5)

gesture_label = tk.Label(panel, text="Gesture: None", bg="#2b2b2b", fg="white", font=("Arial", 12))
gesture_label.pack(pady=5)

hands_label = tk.Label(panel, text="Hands: 0", bg="#2b2b2b", fg="white", font=("Arial", 12))
hands_label.pack(pady=5)

fps_label = tk.Label(panel, text="Detection FPS: 0", bg="#2b2b2b", fg="white", font=("Arial", 12))
fps_label.pack(pady=5)

latency_label = tk.Label(panel, text="Latency: 0 ms", bg="#2b2b2b", fg="white", font=("Arial", 12))
latency_label.pack(pady=5)

model_label = tk.Label(panel, text="Model Status: Not Loaded", bg="#2b2b2b", fg="red", font=("Arial", 12))
model_label.pack(pady=5)

# -------- CURRENT VOLUME DISPLAY --------
tk.Label(panel, text="Current Volume", bg="#010779",
         fg="white", font=("Arial", 12, "bold")).pack(pady=(10,0))

big_volume_label = tk.Label(panel, text="50%",
                            bg="#2b2b2b", fg="lightgreen",
                            font=("Arial", 28, "bold"))
big_volume_label.pack(pady=10)

# -------- PARAMETERS --------
tk.Label(panel, text="Detection Parameters", bg="#010AA3",
         fg="white", font=("Arial", 12, "bold")).pack(pady=(10, 0))
conf_frame = tk.Frame(panel, bg="#2b2b2b")
conf_frame.pack(fill="x")

tk.Label(conf_frame, text="Detection Confidence", bg="#2b2b2b", fg="white").pack(anchor="w")

row = tk.Frame(conf_frame, bg="#2b2b2b")
row.pack(fill="x")

conf_slider = ttk.Scale(row, from_=0.1, to=1.0, orient="horizontal", command=update_conf_label)
conf_slider.set(0.7)
conf_slider.pack(side="left", fill="x", expand=True, padx=5)

conf_value_label = tk.Label(row, text="70%", bg="#2b2b2b", fg="lightgreen", width=5)
conf_value_label.pack(side="right")
# ---------------------------------

track_frame = tk.Frame(panel, bg="#2b2b2b")
track_frame.pack(fill="x")

tk.Label(track_frame, text="Tracking Confidence", bg="#2b2b2b", fg="white").pack(anchor="w")

row2 = tk.Frame(track_frame, bg="#2b2b2b")
row2.pack(fill="x")

track_slider = ttk.Scale(row2, from_=0.1, to=1.0, orient="horizontal", command=update_track_label)
track_slider.set(0.7)
track_slider.pack(side="left", fill="x", expand=True, padx=5)

track_value_label = tk.Label(row2, text="70%", bg="#2b2b2b", fg="lightgreen", width=5)
track_value_label.pack(side="right")
# -------------------------------------

tk.Label(panel, text="Max Hands", bg="#2b2b2b", fg="white").pack()
maxhands_slider = ttk.Scale(panel, from_=1, to=4, orient="horizontal")
maxhands_slider.set(1)
maxhands_slider.pack(pady=3)

# -------- DETECTION INFO --------
tk.Label(panel, text="Detection Info", bg="#010779",
         fg="white", font=("Arial", 12, "bold")).pack(pady=(10, 0))

landmarks_label = tk.Label(panel, text="Landmarks: 21",
                           bg="#2b2b2b", fg="white", font=("Arial", 11))
landmarks_label.pack(pady=3)

connections_label = tk.Label(panel, text="Connections: 20",
                             bg="#2b2b2b", fg="white", font=("Arial", 11))
connections_label.pack(pady=3)

resolution_label = tk.Label(panel, text="Resolution: 0x0",
                            bg="#2b2b2b", fg="white", font=("Arial", 11))
resolution_label.pack(pady=3)

frametime_label = tk.Label(panel, text="Frame Time: 0 ms",
                           bg="#2b2b2b", fg="white", font=("Arial", 11))
frametime_label.pack(pady=3)

# -------- DISTANCE MEASUREMENT --------
tk.Label(panel, text="Distance Measurement", bg="#010AA3",
         fg="white", font=("Arial", 12, "bold")).pack(pady=(10,0))

distance_label = tk.Label(panel, text="0 px",
                          bg="#2b2b2b", fg="cyan", font=("Arial", 16, "bold"))
distance_label.pack(pady=5)

# -------- VOLUME GRAPH --------
tk.Label(panel, text="Distance to Volume Mapping", bg="#010779",
         fg="white", font=("Arial", 12, "bold")).pack(pady=(10,0))

fig, ax = plt.subplots(figsize=(3,3))
ax.set_xlim(0, 200)
ax.set_ylim(0, 100)
ax.set_xlabel("Distance (px)")
ax.set_ylabel("Volume (%)")
ax.grid(True)

line, = ax.plot([], [], color="green")
point, = ax.plot([], [], 'ro')

canvas_graph = FigureCanvasTkAgg(fig, master=panel)
canvas_graph.get_tk_widget().pack()

# -------- GESTURE STATES --------
closed_label = tk.Label(panel, text="Closed  (< 40 px)",
                        bg="#2b2b2b", fg="white", font=("Arial", 11))
closed_label.pack(pady=2)

pinch_label = tk.Label(panel, text="Pinch  (40 – 120 px)",
                       bg="#2b2b2b", fg="white", font=("Arial", 11))
pinch_label.pack(pady=2)

open_label = tk.Label(panel, text="Open Hand  (> 120 px)",
                      bg="#2b2b2b", fg="white", font=("Arial", 11))
open_label.pack(pady=2)

root.mainloop()
