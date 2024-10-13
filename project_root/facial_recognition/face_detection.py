# face_detection.py

import cv2
import sys
import os
import threading
import time  # Import time for sleep control
from camera_module.camera import Camera  # Import the Camera class

class FaceDetector:
    def __init__(self):
        self.camera = None
        self.face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        self.is_running = False

    def start(self):
        try:
            self.camera = Camera()  # Initialize the camera
        except Exception as e:
            print(f"Camera not accessible: {e}")
            return

        self.is_running = True
        threading.Thread(target=self.detect_faces).start()

    def stop(self):
        self.is_running = False

    def detect_faces(self):
        while self.is_running:
            ret, frame = self.camera.read()
            if not ret:
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

            cv2.imshow('Face Detection', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.camera.release()
        cv2.destroyAllWindows()