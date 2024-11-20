# Facial Recognition Project

## Description
This project is designed to perform real time facial recognition using a webcam that compares against  images stored in the images folder. The facial encodings and names of images are saved in an SQLite database named `facial_encodings.db`. This database is then accessed and compared to faces in the view of the camera frame by frame to determine if the face in the view of the camera is identified. If the face is identified a green box with the associated image name is made around the face while simultaneously unlocking the lock. 

This is all displayed in the local browser using a Flask app. In the flask app extra functionallity is added. It includes functions to add faces to the database as well as clear the database of all encodings. As a finishing touch password protection was added when attempting to add faces or clear the database. The password can be adjusted by the host in app.py under UPLOAD_PASSWORD. 

## Installation
1. Clone the repository to your local machine:
    ```sh
    git clone https://github.com/yourusername/Computer-Orginization-Project1.git
    ```
2. Navigate to the project directory:
    ```sh
    cd Computer-Orginization-Project1
    ```
3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Usage
1. Navigate to the project_root directory 
2. In shell run these these three lines in order:
3. hostname -I : to see what the IP of your local Rapsberry PI is 
4. export FLASK_APP=app.py
5. flask run --host=0.0.0.0
6. In your browser navigate to <ip of youre device>:5000
7. From here you have access to the app


## Sources
1. How to set up and compare the faces as well as draw the boxes in real time [here](https://github.com/ageitgey/face_recognition/blob/master/examples/facerec_from_webcam_faster.py).
2. How to get to display the image caputred, with boxes around facesl, by the webcam (in realtime.py) to the flask app [here](https://stackoverflow.com/questions/64579316/python-opencv-flask-videocamera-turning-on-but-not-displaying-video-feed)
3. How to use the face recognition Python module [here](https://pypi.org/project/face-recognition/)
4. How to delete all images in a folder [here](https://www.tutorialspoint.com/how-to-delete-all-files-in-a-directory-with-python#:~:text=The%20versatile%20Python%20os%20module,remove()%20method.)
5. Password protection and session authentication in flask [here](https://syscrews.medium.com/session-based-authentication-in-flask-d43fe36afc0f)
6. Sqlite3 documentation used for the SQL database [here](https://docs.python.org/3/library/sqlite3.html)
7. Setup and use outputs with RIP.GPIO [here](https://raspi.tv/2013/rpi-gpio-basics-5-setting-up-and-using-outputs-with-rpi-gpio)
8. Diyables Arduino Solenoid Lock wiring and partial setup [here](https://arduinogetstarted.com/tutorials/arduino-solenoid-lock)
