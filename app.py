from flask import Flask, render_template, Response
import cv2
import numpy as np
import mediapipe as mp
from math import hypot
import screen_brightness_control as sbc
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL

app = Flask(__name__)

# Audio setup
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
volRange = volume.GetVolumeRange()
minVol, maxVol, _ = volRange

# Setting up hands model
mpHands = mp.solutions.hands
hands = mpHands.Hands(static_image_mode=False, max_num_hands=2, model_complexity=1, min_detection_confidence=0.75, min_tracking_confidence=0.75)
draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

def generate_frames():
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.flip(frame, 1)
        frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        processed = hands.process(frameRGB)

        left_landmark_list, right_landmark_list = get_left_right_landmarks(frame, processed, draw, mpHands)

        # For changing the brightness level
        if left_landmark_list:
            left_distance = get_distance(frame, left_landmark_list)
            b_level = np.interp(left_distance, [30, 200], [0, 100]) 
            sbc.set_brightness(b_level)

        # For changing the volume level
        if right_landmark_list:
            right_distance = get_distance(frame, right_landmark_list)
            vol = np.interp(right_distance, [30, 200], [minVol, maxVol])
            volume.SetMasterVolumeLevel(vol, None)

        # Convert the frame to JPEG
        _, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

def get_left_right_landmarks(frame, processed, draw, mpHands):
    left_landmark_list = []
    right_landmark_list = []

    if processed.multi_hand_landmarks:
        for handlm in processed.multi_hand_landmarks:
            landmarks = []
            for idx, found_landmark in enumerate(handlm.landmark):
                height, width, _ = frame.shape
                x, y = int(found_landmark.x * width), int(found_landmark.y * height)

                if idx == 4 or idx == 8:
                    landmarks.append([idx, x, y])

            # Identify left and right hand based on the position
            if landmarks:
                avg_x = np.mean([lm[1] for lm in landmarks])

                if avg_x < frame.shape[1] // 2:
                    left_landmark_list = landmarks
                else:
                    right_landmark_list = landmarks

            draw.draw_landmarks(frame, handlm, mpHands.HAND_CONNECTIONS)

    return left_landmark_list, right_landmark_list

def get_distance(frame, landmark_list):
    if len(landmark_list) < 2:
        return

    (x1, y1), (x2, y2) = (landmark_list[0][1], landmark_list[0][2]), (landmark_list[1][1], landmark_list[1][2])
    cv2.circle(frame, (x1, y1), 7, (0, 255, 0), cv2.FILLED)
    cv2.circle(frame, (x2, y2), 7, (0, 255, 0), cv2.FILLED)
    cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 3)

    l = hypot(x2 - x1, y2 - y1)
    return l

if __name__ == '__main__':
    app.run(debug=True)
