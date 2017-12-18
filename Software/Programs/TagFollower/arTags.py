#!/usr/bin/python

import numpy as np
import cv2
import tagsLib as tags
import sys
sys.path.append('/home/nanopi')
from NeoBoardClasses import DifferentialDrive
import subprocess

motLA = 7
motLB = 6
motRA = 5
motRB = 4
minSpeed = 10
maxSpeed = 60
wheels = DifferentialDrive(motLA, motLB, motRA, motRB, minSpeed, maxSpeed)

def main():

    camRet = tags.cameraInit()
    capture, imgSize, target = camRet

    while True:
	    direction, speed = (0, 0)
        tagCorners = tags.findTag(capture)
        if tagCorners is not None:
            tagCenter, tagArea = tags.processTagInfo(tagCorners)
            tagPercent = (tagArea * 100) / (imgSize[0] * imgSize[1])
            direction, speed = tags.calcDirSpeed(tagCenter, tagPercent, camRet)
        wheels.drive(-direction, speed)
        print("Direction: {:.2f}, Speed: {:.2f}".format(direction, speed))

        # EXIT
        #if cv2.waitKey(1) & 0xFF == ord('q'):
         #   break

    tags.cameraStop(capture)


if __name__ == "__main__":
    # Start video stream
    #subprocess.call("/home/nanopi/FPV/videoStream.sh &", shell=True)
    main()
