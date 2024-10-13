import cv2
import sys
import os

# Ensure the path to the camera_module is correctly set
camera_module_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../camera_module'))
if camera_module_path not in sys.path:
    sys.path.append(camera_module_path)

from camera import Camera  # Import the Camera class

class FaceDetector:
    def __init__(self):
        # Load the required trained XML classifiers for face and eye detection
        self.face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        self.eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')

        # Initialize the camera
        self.camera = Camera()

    def start_detection(self):
        self.camera.start()  # Start the camera capture
        while True:
            ret, frame = self.camera.capture.read()  # Read frames from the camera

            if not ret:
                print("Error: Could not read frame.")
                break

            # Convert to gray scale for face detection
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # Detect faces in the frame
            faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)

            # Loop through the detected faces
            for (x, y, w, h) in faces:
                # Draw a rectangle around the face
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 255, 0), 2)
                roi_gray = gray[y:y+h, x:x+w]  # Region of interest for gray scale
                roi_color = frame[y:y+h, x:x+w]  # Region of interest for color

                # Detect eyes within the face region
                eyes = self.eye_cascade.detectMultiScale(roi_gray)
                for (ex, ey, ew, eh) in eyes:
                    # Draw a rectangle around the eyes
                    cv2.rectangle(roi_color, (ex, ey), (ex+ew, ey+eh), (0, 127, 255), 2)

            # Display the resulting frame with detections
            cv2.imshow('Camera Feed with Face and Eye Detection', frame)

            # Press 'q' to exit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    def release(self):
        self.camera.release()  # Release the camera

if __name__ == "__main__":
    detector = FaceDetector()
    try:
        detector.start_detection()  # Start face detection
    except Exception as e:
        print(e)
    finally:
        detector.release()  # Release resources