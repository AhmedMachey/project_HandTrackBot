import cv2 
import mediapipe as mp
import numpy as np
import time
import serial

# Set up serial comms between this python script and the Arduino
my_port = "COM6"  # Change this to your port
ser = serial.Serial(my_port, 9600, timeout=1)
ser.flush()

if ser.name:
    port = ser.name
    print(f'Serial comms established on port: {port}')

# Define the colors
WHITE_COLOR = (224, 224, 224)
BLACK_COLOR = (0, 0, 0)
RED_COLOR = (0, 0, 255)
GREEN_COLOR = (0, 128, 0)
BLUE_COLOR = (255, 0, 0)

# Set up MediaPipe for hand tracking
mp_draw = mp.solutions.drawing_utils
draw_specs = mp_draw.DrawingSpec(color=BLUE_COLOR, thickness=2, circle_radius=2)
mp_pose = mp.solutions.hands
pose = mp_pose.Hands(static_image_mode=False,
                     max_num_hands=1,
                     min_detection_confidence=0.85,
                     min_tracking_confidence=0.5)

# Set up webcam capture
cap = cv2.VideoCapture(0)
video_width = 480
video_height = 420
cap.set(3, video_width)
cap.set(4, video_height)

start_time = 0

while True:
    success, image = cap.read()
    image = cv2.flip(image, 1)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = pose.process(image_rgb)

    h, w, c = image.shape
    display_image = image

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            x_list = []
            y_list = []
            fingers_up = [0, 0, 0, 0, 0]

            mp_draw.draw_landmarks(display_image, hand_landmarks, mp_pose.HAND_CONNECTIONS, draw_specs, draw_specs)

            for id, lm in enumerate(hand_landmarks.landmark):
                x = int(lm.x * w)
                y = int(lm.y * h)
                x_list.append(x)
                y_list.append(y)

            # Thumb
            if x_list[4] <= x_list[5]:
                fingers_up[0] = 1
            # Index finger
            if y_list[8] <= y_list[6]:
                fingers_up[1] = 1
            # Middle finger
            if y_list[12] <= y_list[10]:
                fingers_up[2] = 1
            # Ring finger
            if y_list[16] <= y_list[14]:
                fingers_up[3] = 1
            # Pinky finger
            if y_list[20] < y_list[18]:
                fingers_up[4] = 1

            # Determine gesture and send command to Arduino
            gesture_label = ""
            if ser.name:
                if fingers_up == [1, 1, 1, 1, 1]:
                    ser.write(b"F\n")
                    gesture_label = "Right"
                elif fingers_up == [0, 1, 0, 0, 0]:
                    ser.write(b"R\n")
                    gesture_label = "forword"
                elif fingers_up == [0, 1, 1, 0, 0]:
                    ser.write(b"L\n")
                    gesture_label = "Back"
                elif fingers_up == [0, 0, 0, 0, 0]:
                    ser.write(b"S\n")
                    gesture_label = "Stop"
                elif fingers_up == [0, 1, 1, 1, 1]:
                    ser.write(b"B\n")
                    gesture_label = "left"

            # Draw a black rectangle at the top-left corner as a background for the text
            cv2.rectangle(image, (10, 10), (210, 80), BLACK_COLOR, cv2.FILLED)

            # Display the gesture label in red on top of the black rectangle
            cv2.putText(image, gesture_label, (20, 60), cv2.FONT_HERSHEY_PLAIN, 3, RED_COLOR, 3)

    # Get the frame rate
    current_time = time.time()
    fps = 1 / (current_time - start_time)
    start_time = current_time

    # Display the webcam video frame
    cv2.imshow('Video', display_image)

    # Press 'q' on the keyboard to close the video
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cap.release()
cv2.destroyAllWindows()
