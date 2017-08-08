import math
import numpy as np
import cv2

cap = cv2.VideoCapture(0)
dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_ARUCO_ORIGINAL)

# Once to get height and width
ret, frame = cap.read()
frame = cv2.flip(frame,1)
height, width = frame.shape[:2]
side=0

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    # Flip image
    frame = cv2.flip(frame,1)

    # Our operations on the frame come here
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(gray,dictionary)

    # If found
    if len(corners) > 0:
        cv2.aruco.drawDetectedMarkers(gray,corners,ids)
        print(corners)

    # EXIT
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # Display the resulting frame
    cv2.imshow('frame',gray)

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
