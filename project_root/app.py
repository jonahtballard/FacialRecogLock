from flask import Flask, Response, render_template, redirect, url_for
from face_detection import FaceDetector  # Import the FaceDetector class

app = Flask(__name__)
detector = FaceDetector()

@app.route('/')
def index():
    return render_template('index.html')  # Create a template to control the detection

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