# app.py

from flask import Flask, render_template, Response
import cv2
import sys
import os
import threading

app = Flask(__name__)

# Ensure the path to the camera_module is correctly set
camera_module_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'camera_module'))
if camera_module_path not in sys.path:
    sys.path.append(camera_module_path)

from camera import Camera  # Import the Camera class

# Ensure the path to the face_detection_module is correctly set
face_detection_module_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'facial_recognition'))
if face_detection_module_path not in sys.path:
    sys.path.append(face_detection_module_path)

from face_detection import FaceDetector  # Import the FaceDetector class

camera = None  # Global camera variable
face_detector = None  # Global face detector variable

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(face_detector.start_detection(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/start_detection')
def start_detection():
    face_detector.toggle_detection()  # Start face detection
    return ('', 204)  # No content response

@app.route('/stop_detection')
def stop_detection():
    face_detector.toggle_detection()  # Stop face detection
    return ('', 204)  # No content response

if __name__ == '__main__':
    camera = Camera()
    face_detector = FaceDetector()
    detection_thread = threading.Thread(target=face_detector.start_detection)
    detection_thread.start()
    app.run(host='0.0.0.0', port=5000)