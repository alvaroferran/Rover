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
        a= corners[0][0][0][0] - corners[0][0][1][0]
        b= corners[0][0][0][1] - corners[0][0][1][1]
        side= math.sqrt( math.pow(a,2) + math.pow(b,2) )
        percentage= (side*side*100)/(width*height)
        print("Area: %0.2f%%"  % (percentage))
        diagX=(corners[0][0][0][0] + corners[0][0][2][0])/2
        diagY=(corners[0][0][0][1] + corners[0][0][2][1])/2
        center= (diagX, diagY)
        if center[0] > width/2:
            x=1
        else :
            x=-1
        if center[1] > height/2:
            y=-1
        else :
            y=1
        print("Quadrant (%d , %d)" %(x,y))


    # EXIT
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    # Display the resulting frame
    cv2.imshow('frame',gray)

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
