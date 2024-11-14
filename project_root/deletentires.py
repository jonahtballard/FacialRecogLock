import os
import subprocess

folder_path = "../project_root/images"


def delete_images():
    # Get a list of all files in the folder
    files = os.listdir(folder_path)

    # Loop through the files and delete the ones that are images (e.g., jpg, png)
    for file in files:
        file_path = os.path.join(folder_path, file)
        if os.path.isfile(file_path):  # Make sure it's a file
            os.remove(file_path)  # Delete the file
            print(f"Deleted {file}")

delete_images()

db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'db.py')
subprocess.run(['python', db_path])
