import cv2

class Camera:
    def __init__(self, camera_index=0):
        self.camera_index = camera_index
        self.capture = cv2.VideoCapture(self.camera_index)

        if not self.capture.isOpened():
            print(f"Error: Could not open camera with index {self.camera_index}")
            raise Exception("Camera not accessible.")

    def generate_frames(self):
        while True:
            success, frame = self.capture.read()  # Capture frame-by-frame
            if not success:
                break
            else:
                # Encode the frame in JPEG format
                _, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    def release(self):
        self.capture.release()