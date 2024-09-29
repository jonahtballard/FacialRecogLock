import cv2

class Camera:
    def __init__(self, camera_index=0):
        self.camera_index = camera_index
        self.capture = cv2.VideoCapture(self.camera_index)

        if not self.capture.isOpened():
            print(f"Error: Could not open camera with index {self.camera_index}")
            raise Exception("Camera not accessible.")

    def start(self):
        while True:
            # Capture frame-by-frame
            ret, frame = self.capture.read()

            if not ret:
                print("Error: Could not read frame.")
                break

            # Display the resulting frame
            cv2.imshow('Camera Feed', frame)

            # Press 'q' to exit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    def release(self):
        # When everything is done, release the capture
        self.capture.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    cam = Camera()
    try:
        cam.start()
    except Exception as e:
        print(e)
    finally:
        cam.release()