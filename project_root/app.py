import sqlite3
from flask import Flask, flash, render_template, Response, redirect, session, url_for, request
import os
import subprocess
import time
from realtime import load_encodings_from_db, generate_frames


app = Flask(__name__)  

# Secret key for session management (required for flash messages)
app.secret_key = '123bwfyuenoiwe390247y83iubfjnosd'

# Password for accessing the upload page
UPLOAD_PASSWORD = 'jonah'

# Ensure that the 'images' folder exists
image_folder = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'images')
os.makedirs(image_folder, exist_ok=True)

# Global variables to store the encodings and names
known_face_encodings, known_face_names = load_encodings_from_db()
last_updated = time.time()

# Function to update encodings
def refresh_encodings():
    global known_face_encodings, known_face_names, last_updated
    known_face_encodings, known_face_names = load_encodings_from_db()
    last_updated = time.time()

# Use before_request to check if 30 seconds have passed
@app.before_request
def check_for_encoding_refresh():
    global last_updated
    if time.time() - last_updated >= 15:
        refresh_encodings()  # Refresh encodings every 15 seconds

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/clear_database', methods=['POST', 'GET'])
def clear_database():
    if not session.get('upload_authenticated'):
        # If not authenticated, redirect them to the login page
        session['next'] = 'home'  # Store the intended page for after login
        return redirect(url_for('login'))

    if request.method == 'GET':
        db_path2 = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'deletentires.py')
        subprocess.run(['python', db_path2])
        return redirect(url_for('home'))  # Redirect to home after clearing database

    return redirect(url_for('home'))  # If GET, just redirect to home

   
@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(known_face_encodings, known_face_names), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/start_video')
def start_video():
    db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'db.py')
    subprocess.run(['python', db_path])
    return render_template('video.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form.get('password')
        if password == UPLOAD_PASSWORD:
            session['upload_authenticated'] = True  # Store login status for upload
            next_page = session.pop('next', 'home')  # Redirect to the intended page after login
            return redirect(url_for(next_page))
        else:
            flash('Incorrect password. Please try again.')
    return render_template('login.html')

@app.route('/upload_image', methods=['GET', 'POST'])
def upload_image():
    # Check if the user is trying to access the upload page directly
    if not session.get('upload_authenticated'):
        # If not authenticated, redirect them to the login page
        session['next'] = 'upload_image'  # Store the intended page for after login
        return redirect(url_for('login'))
    
    # Handle the image upload process
    if request.method == 'POST':
        image_file = request.files['image']
        if image_file:
            # Save the image to the images directory
            image_path = os.path.join(image_folder, image_file.filename)
            image_file.save(image_path)
            print(f"Image uploaded: {image_path}")

            db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'db.py')
            subprocess.run(['python', db_path])

            db_path1 = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'realtime.py')
            subprocess.run(['python', db_path1])

            return redirect(url_for('home'))
    
    return render_template('upload.html')

@app.route('/logout')
def logout():
    session.pop('upload_authenticated', None)  # Remove the authentication flag for upload
    return redirect(url_for('home'))

@app.route('/back_to_home')
def back_to_home():
    return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(debug=True)
