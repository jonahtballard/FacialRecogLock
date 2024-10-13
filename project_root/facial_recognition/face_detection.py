# face_detection.py

import cv2
import sys
import os
import threading
import time  # Import time for sleep control

# Ensure the path to the camera_module is correctly set
camera_module_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../camera_module'))
if camera_module_path not in sys.path:
    sys.path.append(camera_module_path)

from camera import Camera  # Import the Camera class

class FaceDetector:
    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        self.eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
        self.camera = Camera()  # Instantiate the Camera class
        self.running = False
        self.detection_enabled = False  # Add this variable to track detection state

    def start_detection(self):
        self.running = True
        while self.running:
            frame = self.camera.get_frame()  # Get the current frame from the camera

            if frame is None:
                print("Error: Could not read frame.")
                break

            if self.detection_enabled:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)

                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 255, 0), 2)
                    roi_gray = gray[y:y+h, x:x+w]
                    roi_color = frame[y:y+h, x:x+w]

                    eyes = self.eye_cascade.detectMultiScale(roi_gray)
                    for (ex, ey, ew, eh) in eyes:
                        cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 127, 255), 2)

            cv2.imshow('Camera Feed', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    def toggle_detection(self):
        self.detection_enabled = not self.detection_enabled  # Toggle the detection state

    def stop_detection(self):
        self.running = False
        self.camera.release()  # Release the camera
        cv2.destroyAllWindows()

    def run(self):
        detection_thread = threading.Thread(target=self.start_detection)
        detection_thread.start()