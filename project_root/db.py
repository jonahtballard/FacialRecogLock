import face_recognition
import sqlite3
import numpy as np
import os

# Folder containing images
folder_path = "/Users/jonahballard/Documents/Computer-Orginization-Project1/project_root/images/"
db_path = os.path.join(folder_path, '../facial_encodings.db')

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS encodings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        image_name TEXT,
        encoding BLOB
    )
''')

# Clear old encodings and insert new ones
cursor.execute('DELETE FROM encodings')

for filename in os.listdir(folder_path):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        image_path = os.path.join(folder_path, filename)
        image = face_recognition.load_image_file(image_path)
        face_encodings = face_recognition.face_encodings(image)

        if face_encodings:
            encoding = face_encodings[0]
            encoding_list = encoding.tolist()

            cursor.execute('''
                INSERT INTO encodings (image_name, encoding) VALUES (?, ?)
            ''', (filename, sqlite3.Binary(np.array(encoding_list).tobytes())))
            print(f"Facial encoding for '{filename}' stored.")
        else:
            print(f"No faces found in '{filename}'.")

conn.commit()
conn.close()
