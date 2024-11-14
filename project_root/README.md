# Facial Recognition Project

## Description
This project is designed to perform facial recognition using images stored in a specified folder. The facial encodings are saved in an SQLite database named `facial_encodings.db` located in the project root directory.

## Installation
1. Clone the repository to your local machine:
    ```sh
    git clone https://github.com/yourusername/facial-recognition-project.git
    ```
2. Navigate to the project directory:
    ```sh
    cd facial-recognition-project
    ```
3. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Usage
1. Ensure your images are stored in the `images` folder within the project root directory.
2. Run the script to process the images and save the facial encodings to the database:
    ```sh
    python script_name.py
    ```
3. The facial encodings will be saved in `facial_encodings.db` in the project root directory.

## Source
This project is based on the example code from the `face_recognition` library. You can find the original source code [here](https://github.com/ageitgey/face_recognition/blob/master/examples/facerec_from_webcam_faster.py).
