# face_detection.py

import cv2
import sys
import os
import threading
import time  # Import time for sleep control
from camera_module.camera import Camera  # Import the Camera class

class FaceDetector:

    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.camera = Camera()  # Initialize the camera
        self.face_detection_enabled = False  # Flag to enable/disable face detection
        self.thread = threading.Thread(target=self.detect_faces)  # Create a thread for face detection
        self.thread.daemon = True  # Set the thread as a daemon
        self.thread.start()  # Start the thread

    def detect_faces(self):
        while True:
            if self.face_detection_enabled:
                frame = self.camera.capture.read()[1]  # Capture frame-by-frame
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Convert the frame to grayscale
                faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))  # Detect faces
                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)  # Draw a rectangle around the face
                _, buffer = cv2.imencode('.jpg', frame)  # Encode the frame in JPEG format
                frame = buffer.tobytes()
                self.camera.frame = frame  # Update the frame in the camera object
            else:
                time.sleep(0.1)  # Sleep for 100ms if face detection is disabled

    def toggle_detection(self):
        self.face_detection_enabled = not self.face_detection_enabled  # Toggle the face detection flag

    def release(self):
        self.camera.release()  # Release the camera