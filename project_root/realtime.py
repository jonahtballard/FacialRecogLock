import subprocess
import face_recognition
import cv2
import sqlite3
import numpy as np


print("Updating the database with new face encodings...")
subprocess.run(['python', 'db.py'])



def load_encodings_from_db():
    # Connect to the SQLite database
    conn = sqlite3.connect('facial_encodings.db')
    cursor = conn.cursor()

    # Fetch all image names and encodings from the database
    cursor.execute('SELECT image_name, encoding FROM encodings')
    data = cursor.fetchall()
    conn.close()

    known_face_encodings = []
    known_face_names = []

    # Convert each encoding back to a numpy array
    for image_name, encoding in data:
        # Convert byte data back into a numpy array
        encoding = np.frombuffer(encoding, dtype=np.float64)
        known_face_encodings.append(encoding)
        known_face_names.append(image_name)

    return known_face_encodings, known_face_names




known_face_encodings, known_face_names = load_encodings_from_db()


# Initialize the webcam
video_capture = cv2.VideoCapture(0)  

while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()

    if not ret:
        print("Failed to grab frame.")
        break

    # Find all face locations and encodings in the current frame
    face_locations = face_recognition.face_locations(frame)
    face_encodings = face_recognition.face_encodings(frame, face_locations)

    # Initialize an array to hold the names of people detected in the current frame
    face_names = []

    for face_encoding in face_encodings:
        # Check if the face matches any known faces
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)

        name = "Unknown"

        # If a match is found, use the name of the matching face
        if True in matches:
            first_match_index = matches.index(True)
            name = known_face_names[first_match_index]

        face_names.append(name)

    for (top, right, bottom, left), name in zip(face_locations, face_names):
        if name == "Unknown":
            # If the person is unknown, use a red rectangle
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)  # Red color
        else:
            # If the person is recognized, use a green rectangle
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)  # Green color
        
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1, (255, 255, 255), 1)

    # Display the resulting image
    cv2.imshow('Video', frame)

    # Press 'q' to quit the video stream
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close all OpenCV windows
video_capture.release()
cv2.destroyAllWindows()

