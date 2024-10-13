import cv2
import sys
import os
import threading
import time

# Ensure the path to the camera_module is correctly set
camera_module_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../camera_module'))
if camera_module_path not in sys.path:
    sys.path.append(camera_module_path)

from camera import Camera  # Import the Camera class

class FaceDetector:
    def __init__(self):
        self.face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        self.eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
        self.camera = Camera()
        self.running = False

    def start_detection(self):
        self.running = True
        self.camera.start()  # Start the camera capture
        while self.running:
            ret, frame = self.camera.capture.read()  # Read frames from the camera

            if not ret:
                print("Error: Could not read frame.")
                break

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)

            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 255, 0), 2)
                roi_gray = gray[y:y+h, x:x+w]
                roi_color = frame[y:y+h, x:x+w]

                eyes = self.eye_cascade.detectMultiScale(roi_gray)
                for (ex, ey, ew, eh) in eyes:
                    cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 127, 255), 2)

            cv2.imshow('Camera Feed with Face and Eye Detection', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    def stop_detection(self):
        self.running = False
        self.camera.release()  # Release the camera
        cv2.destroyAllWindows()

    def run(self):
        detection_thread = threading.Thread(target=self.start_detection)
        detection_thread.start()