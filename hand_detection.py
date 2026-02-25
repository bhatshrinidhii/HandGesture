import cv2
import mediapipe as mp
import math
import numpy as np

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

cap = cv2.VideoCapture(0)

volume_percent = 50  # initial volume

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    vol_bar = np.interp(volume_percent, [0, 100], [400, 150])

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:

            mp_draw.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )

            h, w, c = frame.shape
            lm_list = []

            for id, lm in enumerate(hand_landmarks.landmark):
                cx, cy = int(lm.x * w), int(lm.y * h)
                lm_list.append((cx, cy))

            # Finger tips
            fingers = []

            # Thumb (special case, check x direction)
            if lm_list[4][0] > lm_list[3][0]:
                fingers.append(1)
            else:
                fingers.append(0)

            # Other fingers
            tips = [8, 12, 16, 20]
            pips = [6, 10, 14, 18]

            for tip, pip in zip(tips, pips):
                if lm_list[tip][1] < lm_list[pip][1]:
                    fingers.append(1)
                else:
                    fingers.append(0)

            total_fingers = fingers.count(1)

            # ----------- GESTURE LOGIC ------------

            # FIST → MUTE
            if total_fingers == 0:
                volume_percent = 0
                cv2.putText(frame, "MUTE",
                            (200, 100),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            2,
                            (0, 0, 255),
                            4)

            # # 2 FINGERS (INDEX + MIDDLE) → +10%
            # elif fingers[1] == 1 and fingers[2] == 1 and total_fingers == 2:
            #     volume_percent = min(100, volume_percent + 10)
            #     cv2.putText(frame, "Volume +10%",
            #                 (150, 100),
            #                 cv2.FONT_HERSHEY_SIMPLEX,
            #                 1,
            #                 (0, 255, 0),
            #                 3)

            # # 3 FINGERS (INDEX + MIDDLE + RING) → -10%
            # elif fingers[1] == 1 and fingers[2] == 1 and fingers[3] == 1 and total_fingers == 3:
            #     volume_percent = max(0, volume_percent - 10)
            #     cv2.putText(frame, "Volume -10%",
            #                 (150, 100),
            #                 cv2.FONT_HERSHEY_SIMPLEX,
            #                 1,
            #                 (255, 0, 0),
            #                 3)

            # Smooth Control (Thumb + Index)
            else:
                x1, y1 = lm_list[4]
                x2, y2 = lm_list[8]

                cv2.circle(frame, (x1, y1), 8, (0, 255, 0), cv2.FILLED)
                cv2.circle(frame, (x2, y2), 8, (0, 0, 255), cv2.FILLED)
                cv2.line(frame, (x1, y1), (x2, y2), (255, 0, 0), 3)

                length = math.hypot(x2 - x1, y2 - y1)
                volume_percent = int(np.interp(length, [20, 200], [0, 100]))

    # -------- DRAW VOLUME BAR --------

    vol_bar = np.interp(volume_percent, [0, 100], [400, 150])

    cv2.rectangle(frame, (50, 150), (85, 400), (0, 255, 0), 3)
    cv2.rectangle(frame, (50, int(vol_bar)), (85, 400), (0, 255, 0), cv2.FILLED)

    cv2.putText(frame, f'{volume_percent} %',
                (40, 450),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 255),
                3)

    cv2.imshow("Gesture Volume Control", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
