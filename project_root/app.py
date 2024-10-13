from flask import Flask, Response
from camera_module.camera import Camera  # Import the Camera class
from facial_recognition.face_detection import FaceDetector  # Import the FaceDetector class


app = Flask(__name__)
camera = Camera()  # Initialize the camera
face_detector = FaceDetector()  # Initialize the face detector

@app.route('/video_feed')
def video_feed():
    return Response(camera.generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/toggle_face_detection')
def toggle_face_detection():
    face_detector.toggle_detection()  # Toggle face detection on/off
    return f'Face detection toggled: {face_detector.is_detection_enabled()}'

@app.route('/')
def index():
    return '<h1>Camera Stream</h1><img src="/video_feed">' 
'<p><a href="/toggle_face_detection">Toggle Face Detection</a></p>'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)