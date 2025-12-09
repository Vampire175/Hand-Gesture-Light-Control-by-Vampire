import cv2
import mediapipe as mp
import serial
import time
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import platform
import subprocess

try:
    import pyudev  # Linux only
except:
    pyudev = None

from datetime import datetime

current_year = datetime.now().year

# ============================================
#          CROSS PLATFORM CAMERA SCAN
# ============================================
def get_all_cameras():
    cameras = []
    os_name = platform.system()

    # ========== WINDOWS ==========
    if os_name == "Windows":
        detected = []
        for i in range(10):
            test = cv2.VideoCapture(i)
            if test.isOpened():
                detected.append(i)
            test.release()

        try:
            result = subprocess.check_output(
                'wmic path Win32_PnPEntity where "Service=\'usbvideo\'" get Name',
                shell=True
            ).decode().strip().split("\n")
            names = [x.strip() for x in result[1:] if x.strip()]
        except:
            names = [f"Camera {i}" for i in detected]

        for index, cam_index in enumerate(detected):
            name = names[index] if index < len(names) else f"Camera {cam_index}"
            cameras.append((cam_index, name))

    # ========== LINUX ==========
    elif os_name == "Linux" and pyudev is not None:
        context = pyudev.Context()
        for device in context.list_devices(subsystem="video4linux"):
            node = device.device_node   # /dev/video0
            if not node:
                continue

            try:
                index = int(node.replace("/dev/video", ""))
            except:
                continue

            name = (device.get('ID_V4L_PRODUCT') or
                    device.get('ID_MODEL') or
                    "Linux Camera")

            cameras.append((index, name))

    # ========== MACOS / FALLBACK ==========
    else:
        for i in range(10):
            test = cv2.VideoCapture(i)
            if test.isOpened():
                cameras.append((i, f"Camera {i}"))
            test.release()

    return cameras


# ============================================
#             CAMERA SELECTION UI
# ============================================
def choose_camera():
    cam_window = tk.Toplevel(window)
    cam_window.title("Select Camera")

    cams = get_all_cameras()

    if not cams:
        tk.Label(cam_window, text="No cameras detected").pack()
        return

    tk.Label(cam_window, text="Select a Camera:", font=("Arial", 12)).pack(pady=5)

    for index, name in cams:
        tk.Button(
            cam_window,
            text=f"{name} (index {index})",
            command=lambda i=index, w=cam_window: select_camera(i, w)
        ).pack(pady=4)


def select_camera(index, win):
    global cap
    win.destroy()

    if cap:
        cap.release()

    cap = cv2.VideoCapture(index)
    messagebox.showinfo("Camera", f"Camera {index} connected")


# ============================================
#       MEDIAPIPE + ARDUINO + TKINTER
# ============================================

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_drawing = mp.solutions.drawing_utils

arduino = None
cap = None


def detect_fingers(hand_landmarks):
    finger_tips = [8, 12, 16, 20]
    thumb_tip = 4
    finger_states = [0, 0, 0, 0, 0]

    if hand_landmarks.landmark[thumb_tip].x < hand_landmarks.landmark[thumb_tip - 1].x:
        finger_states[0] = 1

    for idx, tip in enumerate(finger_tips):
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y:
            finger_states[idx + 1] = 1

    return finger_states


def start_hand_tracking():
    global arduino, cap

    com_port = com_entry.get().strip()
    if not com_port:
        messagebox.showerror("Error", "Please enter a COM port")
        return

    try:
        arduino = serial.Serial("COM"+com_port, 9600, timeout=1)
        time.sleep(2)
    except Exception as e:
        messagebox.showerror("Error", f"Could not open {com_port}: {e}")
        return

    com_entry.config(state="disabled")
    start_button.config(state="disabled")

    if not cap:
        cap = cv2.VideoCapture(0)

    update_frame()


def update_frame():
    global cap, arduino

    if not cap:
        window.after(10, update_frame)
        return

    success, frame = cap.read()
    if not success:
        window.after(10, update_frame)
        return

    frame = cv2.cvtColor(cv2.flip(frame, 1), cv2.COLOR_BGR2RGB)

    results = hands.process(frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            fingers = detect_fingers(hand_landmarks)
            finger_label.config(text=f"Fingers: {fingers}")

            try:
                arduino.write(bytes(fingers))
            except:
                pass
    else:
        finger_label.config(text="Fingers: [0,0,0,0,0]")

    img = Image.fromarray(frame)
    imgtk = ImageTk.PhotoImage(image=img)
    video_label.imgtk = imgtk
    video_label.configure(image=imgtk)

    window.after(10, update_frame)


def on_closing():
    if cap:
        cap.release()
    if arduino:
        arduino.close()
    window.destroy()


# ============================================
#                  UI SETUP
# ============================================
window = tk.Tk()
window.title("Hand Tracking + Camera Selector")

tk.Label(window, text="Enter COM Port:").pack()
com_entry = tk.Entry(window)
com_entry.pack()

start_button = tk.Button(window, text="Start Hand Tracking", command=start_hand_tracking)
start_button.pack(pady=4)

cam_button = tk.Button(window, text="Connect Camera", command=choose_camera)
cam_button.pack(pady=4)

video_label = tk.Label(window)
video_label.pack()

finger_label = tk.Label(window, text="Fingers: [0,0,0,0,0]", font=("Arial", 16))
finger_label.pack(pady=5)

bottom_text = tk.Label(
    window,
    text="© "+str(current_year)+" Vampire Studios - All Rights Reserved",
    background="#040404",
    foreground='#777777',
    font=('Segoe UI Italic', 10, 'italic'),
    anchor='e'
)
bottom_text.place(relx=1.0, rely=1.0, anchor='se', x=-10, y=-10)

window.protocol("WM_DELETE_WINDOW", on_closing)
window.mainloop()
