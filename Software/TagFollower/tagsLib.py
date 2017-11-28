#!/usr/bin/env python

import numpy as np
import cv2
import utilsLib as utils


def cameraInit():

    cap = cv2.VideoCapture(0)   # Use camera as source

    # Get image height and width
    ret, frame = cap.read()  # Capture frame-by-frame
    # frame = cv2.flip(frame, 1)  # Flip image
    height, width = frame.shape[:2]

    # Target window width
    windowScale = 0.1
    windowMin = width/2 - int(width * windowScale)
    windowMax = width/2 + int(width * windowScale)

    values = [cap, [height, width], [windowMin, windowMax]]

    return values


def cameraStop(cap):

    # Release the capture
    cap.release()
    cv2.destroyAllWindows()


def findTag(cap):

    # Set AR tag dictionary
    arSet = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_ARUCO_ORIGINAL)

    # Capture frame-by-frame
    ret, frame = cap.read()

    # Turn frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.flip(gray, 1)  # Flip image

    # Get image height and width
    height, width = gray.shape[:2]

    # Calculate target window width
    windowScale = 0.1
    windowMin = width/2 - int(width * windowScale)
    windowMax = width/2 + int(width * windowScale)

    # Detect tags
    corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(gray, arSet)

    # Draw target window lines
    cv2.line(gray, (width / 2, 0), (width / 2, height), (255, 0, 0), 2)
    cv2.line(gray, (windowMin, 0), (windowMin, height), (255, 0, 0), 1)
    cv2.line(gray, (windowMax, 0), (windowMax, height), (255, 0, 0), 1)

    # Display the frame
    cv2.imshow('Camera', gray)

    # If tag found
    if len(corners) > 0:
        # Draw box around tag
        cv2.aruco.drawDetectedMarkers(gray, corners, ids)
        # Display again to show the box
        cv2.imshow('Camera', gray)
        return corners


def processTagInfo(cors):

    # Convert list to np array
    # [tag, corners, row, coordinate]
    npCorners = np.asarray(cors)

    # X and Y distances of two consecutive points, for all tags
    a = npCorners[:, 0, 0, :] - npCorners[:, 0, 1, :]
    # Length between the two previous points, for all tags
    side = np.sqrt(np.power(a[:, 0], 2)+np.power(a[:, 1], 2))
    # Areas of tags.
    area = np.power(side, 2)

    # Half of X and Y distances of opposing corners, for all tags
    center = (npCorners[:, 0, 0, :] + npCorners[:, 0, 2, :]) / 2

    return (center, area)


def calcDirSpeed(center, percent, ret):

    screen = ret[1]
    target = ret[2]

    # Follow tag until it occupies this percentage of the image
    percentMax = 5

    # Get indexes of tags sorted by ascending order
    orderedIndx = np.argsort(-percent)

    # Take largest tag
    perc = percent[orderedIndx[0]]
    cent = center[orderedIndx[0]]

    if perc < percentMax:
        speed = utils.map(perc, 0, percentMax, 1, 0)
    else:
        speed = 0
        # If tag is too big, go to the next one
        if len(orderedIndx) > 1:
            perc = percent[orderedIndx[1]]
            cent = center[orderedIndx[1]]
            if perc < percentMax:
                speed = utils.map(perc, 0, percentMax, 1, 0)
            else:
                speed = 0

    if cent[0] < target[0]:
        direction = utils.map(cent[0], 0, target[0], -1, 0)
    elif cent[0] > target[1]:
        direction = utils.map(cent[0], target[1], screen[1], 0, 1)
    else:
        direction = 0

    return (direction, speed)
