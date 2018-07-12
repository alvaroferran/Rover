#!/usr/bin/python


import numpy as np
import cv2


class Camera:

    """
    Class to control the rover's camera functions
    """

    def __init__(self):
        pass

    def detectTag(self):
        """
        Check for AR tags and return the largest's ID, corner and center
        coordinates and area, or None if none found
        """
        ret, frame = self.cap.read()  # Capture frame-by-frame
        if ret is True:
            # Turn frame to grayscale
            self.imgGrayscale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            self.imgGrayscale = cv2.flip(self.imgGrayscale, 1)  # Flip image
            # Detect tags
            corners, tagID, rejectedImgPoints = cv2.aruco.detectMarkers(
                                                 self.imgGrayscale, self.arSet)
            # If tag found
            if len(corners) > 0:
                center, area = self.__processTagInfo(corners)
                return (center, area)

    def startCamera(self):
        """
        Select image source and start camera
        """
        # Select camera source
        self.cap = cv2.VideoCapture(0)
        # Set AR tag dictionary
        self.arSet = cv2.aruco.getPredefinedDictionary(
                     cv2.aruco.DICT_ARUCO_ORIGINAL)
        # Get camera height and width
        ret, frame = self.cap.read()  # Capture frame-by-frame
        self.height, self.width = frame.shape[:2]

    def stopCamera(self):
        """
        Release camera
        """
        self.cap.release()

    def __processTagInfo(self, cors):
        """
        Return the largest tag's area and center of gravity from a list of
        corner coordinates
        """
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
        # Take largest tag
        orderedIndx = np.argsort(-area)
        areaLargest = area[orderedIndx[0]]
        centLargest = center[orderedIndx[0]]
        return (centLargest, areaLargest)
