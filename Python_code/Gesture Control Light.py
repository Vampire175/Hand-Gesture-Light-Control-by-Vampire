import cv2
import mediapipe as mp
import serial
import time
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk

from datetime import datetime


current_year = datetime.now().year

# Initialize Mediapipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_drawing = mp.solutions.drawing_utils

arduino = None
cap = None

# Function to detect individual fingers (1 for up, 0 for down)
def detect_fingers(hand_landmarks):
    finger_tips = [8, 12, 16, 20]  # Index, Middle, Ring, Pinky
    thumb_tip = 4
    finger_states = [0, 0, 0, 0, 0]  # Thumb, Index, Middle, Ring, Pinky

    # Check thumb
    if hand_landmarks.landmark[thumb_tip].x < hand_landmarks.landmark[thumb_tip - 1].x:
        finger_states[0] = 1  # Thumb is up

    # Check the other fingers
    for idx, tip in enumerate(finger_tips):
        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y:
            finger_states[idx + 1] = 1  # Other fingers are up

    return finger_states

def start_hand_tracking():
    global arduino, cap
    com_port = com_entry.get().strip()
    if not com_port:
        messagebox.showerror("Error", "Please enter a COM port")
        return

    try:
        arduino = serial.Serial(port=com_port, baudrate=9600, timeout=1)
        time.sleep(2)  # Wait to initialize serial
    except Exception as e:
        messagebox.showerror("Error", f"Could not connect to {com_port}: {e}")
        return

    # Disable the input and start button
    com_entry.config(state='disabled')
    start_button.config(state='disabled')

    cap = cv2.VideoCapture(0)
    update_frame()

def update_frame():
    global cap, arduino
    success, image = cap.read()
    if not success:
        window.after(10, update_frame)
        return

    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
    results = hands.process(image)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            fingers_state = detect_fingers(hand_landmarks)
            finger_label.config(text=f"Fingers State: {fingers_state}")
            try:
                arduino.write(bytes(fingers_state))
            except Exception as e:
                print(f"Error sending to Arduino: {e}")
    else:
        finger_label.config(text="Fingers State: [0,0,0,0,0]")

    img = Image.fromarray(image)
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

# Initialize Tkinter window
window = tk.Tk()
window.title("Hand Tracking with COM Port Input")

tk.Label(window, text="Enter COM Port:").pack()
com_entry = tk.Entry(window)
com_entry.pack()

start_button = tk.Button(window, text="Start", command=start_hand_tracking)
start_button.pack()

video_label = tk.Label(window)
video_label.pack()

finger_label = tk.Label(window, text="Fingers State: [0,0,0,0,0]", font=("Arial", 16))
finger_label.pack()

# Add bottom right copyright text
bottom_text = tk.Label(window,
           text="© "+str(current_year)+" Vampire Studios - All Rights Reserved",
                   background="#040404",
                   foreground='#777777',   # gray color
                   font=('Segoe UI Italic', 10, 'italic'),
                   anchor='e')
bottom_text.place(relx=1.0, rely=1.0, anchor='se', x=-10, y=-10)

window.protocol("WM_DELETE_WINDOW", on_closing)
window.mainloop()
