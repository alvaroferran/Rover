#!/usr/bin/env python

import math
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

    a = cors[0][0][0][0] - cors[0][0][1][0]  # Delta X coord of two corners
    b = cors[0][0][0][1] - cors[0][0][1][1]  # Delta Y coord of two corners
    side = math.sqrt(math.pow(a, 2) + math.pow(b, 2))
    area = math.pow(side, 2)

    centerX = (cors[0][0][0][0] + cors[0][0][2][0]) / 2
    centerY = (cors[0][0][0][1] + cors[0][0][2][1]) / 2
    center = (centerX, centerY)

    return (center, area)


def calcDirSpeed(center, percent, ret):

    # Follow tag until it occupies this percentage of the image
    percentMax = 5

    screen = ret[1]
    target = ret[2]

    if center[0] < target[0]:
        direction = utils.doubleMap(center[0], 0, target[0], -1, 0)
    elif center[0] > target[1]:
        direction = utils.doubleMap(center[0], target[1], screen[1], 0, 1)
    else:
        direction = 0

    if percent < percentMax:
        speed = utils.doubleMap(percent, 0, percentMax, 1, 0)
    else:
        speed = 0

    return (direction, speed)
