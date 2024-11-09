from flask import Flask, render_template, Response, redirect, url_for, request
import os
from realtime import load_encodings_from_db, generate_frames
import subprocess

app = Flask(__name__)

# Ensure that the 'images' folder exists
image_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'images')
os.makedirs(image_folder, exist_ok=True)

# Load known encodings
known_face_encodings, known_face_names = load_encodings_from_db()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(known_face_encodings, known_face_names), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/start_video')
def start_video():
    return render_template('video.html')

@app.route('/upload_image', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        image_file = request.files['image']
        if image_file:
            # Save the image to the images directory
            image_path = os.path.join(image_folder, image_file.filename)
            image_file.save(image_path)
            print(f"Image uploaded: {image_path}")
            subprocess.run(['python3', 'db.py'])

            return redirect(url_for('home'))
    return render_template('upload.html')

@app.route('/back_to_home')
def back_to_home():
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)
