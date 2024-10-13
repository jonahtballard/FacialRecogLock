# camera.py

import cv2

class Camera:
    def __init__(self, camera_index=1):
        self.camera_index = camera_index
        self.capture = cv2.VideoCapture(self.camera_index)

        if not self.capture.isOpened():
            print(f"Error: Could not open camera with index {self.camera_index}")
            raise Exception("Camera not accessible.")

    def get_frame(self):
        success, frame = self.capture.read()  # Capture frame-by-frame
        if not success:
            return None
        return frame

    def release(self):
        self.capture.release()