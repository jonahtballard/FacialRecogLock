from flask import Flask, Response
from camera_module.camera import Camera  # Import the Camera class

app = Flask(__name__)
camera = Camera()  # Initialize the camera

@app.route('/video_feed')
def video_feed():
    return Response(camera.generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/')
def index():
    return '<h1>Camera Stream</h1><img src="/video_feed">'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)