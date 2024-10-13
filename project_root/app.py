import sys
import os

# Add the project root directory to sys.path
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from flask import Flask, Response, render_template, redirect, url_for
from camera_module.camera import Camera  # Import the Camera class from the camera_module directory
from facial_recognition.face_detection import FaceDetector  # Import the FaceDetector class from the facial_recognition directory

app = Flask(__name__)
camera = Camera()  # Instantiate the Camera class
detector = FaceDetector()



@app.route('/')
def index():
    return render_template('index.html')  # Create a template to control the detection

@app.route('/video_feed')
def video_feed():
    return Response(camera.generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/start_detection')
def start_detection():
    detector.run()  # Start face detection
    return redirect(url_for('index'))

@app.route('/stop_detection')
def stop_detection():
    detector.stop_detection()  # Stop face detection
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)