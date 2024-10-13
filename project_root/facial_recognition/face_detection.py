import cv2
import threading
from camera_module.camera import Camera

class FaceDetector:
    def __init__(self):
        self.camera = Camera()
        self.face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        self.is_running = False
        self.frame_with_faces = None  # Store the frame with detected faces

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

            self.frame_with_faces = frame  # Store the frame with detected faces

        self.camera.release()

    def toggle_detection(self):
        if self.is_running:
            self.stop()
        else:
            self.start()

    def is_detection_enabled(self):
        return self.is_running

    def get_frame_with_faces(self):
        return self.frame_with_faces