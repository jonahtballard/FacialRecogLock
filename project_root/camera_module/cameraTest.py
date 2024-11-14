import cv2

camera = cv2.VideoCapture(0)  # Change index if necessary

if not camera.isOpened():
    print("Error: Camera not accessible.")
else:
    ret, frame = camera.read()
    if ret:
        cv2.imshow('Test Frame', frame)
        cv2.waitKey(0)
    else:
        print("Error: Unable to capture image.")

camera.release()
cv2.destroyAllWindows()
