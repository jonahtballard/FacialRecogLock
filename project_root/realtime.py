import face_recognition
import cv2
import sqlite3
import numpy as np
import os


project_root = '../project_root/'

db_path = os.path.join(project_root, 'facial_encodings.db')


# Load encodings from the database
def load_encodings_from_db():
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT image_name, encoding FROM encodings')
    data = cursor.fetchall()
    conn.close()

    known_face_encodings = []
    known_face_names = []
    for image_name, encoding in data:
        encoding = np.frombuffer(encoding, dtype=np.float64)
        known_face_encodings.append(encoding)
        known_face_names.append(image_name)

    return known_face_encodings, known_face_names

known_face_encodings, known_face_names = load_encodings_from_db()

# Video capture and face recognition
def generate_frames(known_face_encodings, known_face_names):
    video_capture = cv2.VideoCapture(0)

    while True:
        ret, frame = video_capture.read()
        if not ret:
            break

        face_locations = face_recognition.face_locations(frame)
        face_encodings = face_recognition.face_encodings(frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"
            if True in matches:

                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]
            face_names.append(name)

        for (top, right, bottom, left), name in zip(face_locations, face_names):
            color = (0, 255, 0) if name != "Unknown" else (0, 0, 255)
            cv2.rectangle(frame, (left, top), (right, bottom), color, 2)
            cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 255, 255), 1)

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    video_capture.release()
