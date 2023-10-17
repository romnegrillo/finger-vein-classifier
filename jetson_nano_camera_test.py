import numpy as np
import cv2

cap = cv2.VideoCapture("nvarguscamerasrc ! nvvidconv ! video/x-raw, width=1024, height=576, format=BGRx ! videoconvert ! video/x-raw, format=BGR ! appsink", cv2.CAP_GSTREAMER)

if cap.isOpened():
    while(True):
        # Capture frame-by-frame
        ret, im= cap.read()

        # Display the resulting frame
        cv2.imshow('frame', im)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
else:
    print("camera open failed")

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()


