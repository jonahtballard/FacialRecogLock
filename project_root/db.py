import face_recognition
import cv2
import sqlite3
import numpy as np
import os

# Specify the folder containing images
folder_path = "/Users/jonahballard/Downloads/Images"  # Change this to your folder path

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('facial_encodings.db')
cursor = conn.cursor()

# Create a table to store encodings if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS encodings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        image_name TEXT,
        encoding BLOB
    )
''')

# Clear the database table before inserting new data
cursor.execute('DELETE FROM encodings')

# Iterate through all files in the specified folder
for filename in os.listdir(folder_path):
    if filename.lower().endswith(('.png', '.jpg', '.jpeg')):  # Process image files only
        image_path = os.path.join(folder_path, filename)  # Get full image path
        image = face_recognition.load_image_file(image_path)

        # Generate facial encodings
        face_encodings = face_recognition.face_encodings(image)

        if len(face_encodings) > 0:
            encoding = face_encodings[0]  # Use the first encoding if multiple faces are found

            # Convert the encoding to a list for storage
            encoding_list = encoding.tolist()

            # Insert the encoding and image name into the database
            cursor.execute('''
                INSERT INTO encodings (image_name, encoding) VALUES (?, ?)
            ''', (filename, sqlite3.Binary(np.array(encoding_list).tobytes()),))

            print(f"Facial encoding for '{filename}' stored successfully.")
        else:
            print(f"No faces found in the image '{filename}'.")

# Commit the changes for the new encodings
conn.commit()

# Load known face encodings from the database
def load_encodings_from_db():
    cursor.execute('SELECT image_name, encoding FROM encodings')
    data = cursor.fetchall()

    known_face_encodings = []
    known_face_names = []

    for image_name, encoding in data:
        # Convert the binary encoding back to a numpy array
        known_face_encodings.append(np.frombuffer(encoding, dtype=np.float64))
        known_face_names.append(image_name)

    return known_face_encodings, known_face_names

# Fetch known face encodings and names from the database
known_face_encodings, known_face_names = load_encodings_from_db()

# Close the database connection
conn.close()

# Print known face encodings and names
print("\nKnown Face Encodings and Names:")
for name, encoding in zip(known_face_names, known_face_encodings):
    print(f"Name: {name}, Encoding: {encoding}")


