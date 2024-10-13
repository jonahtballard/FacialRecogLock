# face_detection.py

import cv2
import sys
import os
import threading
import time  # Import time for sleep control
from camera_module.camera import Camera  # Import the Camera class

class FaceDetector:
    def __init__(self):
        self.camera = Camera()  # Create an instance of the Camera class
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')  # Load the face cascade classifier

    def detect_faces(self):
        while True:
            frame = self.camera.get_frame()  # Get a frame from the camera
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Convert the frame to grayscale

            faces = self.face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))  # Detect faces in the frame

            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)  # Draw a rectangle around each face

            cv2.imshow('Facial Detection', frame)  # Display the frame with facial detection

            if cv2.waitKey(1) & 0xFF == ord('q'):  # Exit if 'q' is pressed
                break

        cv2.destroyAllWindows()  # Close all windows