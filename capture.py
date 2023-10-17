import os
from datetime import datetime
import cv2
 

# Directory to save the images, you can change it depending
# on the dataset you are gathering.
SAVE_DIR = "dataset/with_veins"
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR

# Open a connection to the camera (usually the default camera is 0)
cap = cv2.VideoCapture("nvarguscamerasrc ! nvvidconv ! video/x-raw, width=1024, height=576, format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink", cv2.CAP_GSTREAMER)

if not cap.isOpened():
    print("Could not open the camera!")
    exit()

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Check if frame is captured successfully
    if not ret:
        print("Failed to grab frame!")
        break

    # Display the captured frame
    cv2.imshow("Camera Stream", frame)

    # Wait for the user to press a key and check if it's the 'Enter' key
    key = cv2.waitKey(1)
    if key == 13:  # 13 is the ASCII value for 'Enter'
        # Save the image with a filename based on the current date and time
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        img_name = os.path.join(SAVE_DIR, f"{timestamp}.jpg")
        cv2.imwrite(img_name, frame)
        print(f"Saved image as {img_name}")

    # Break the loop if the 'q' key is pressed
    elif key == 113:  # 113 is the ASCII value for 'q'
        break

# Release the camera and close any OpenCV windows
cap.release()
cv2.destroyAllWindows()
