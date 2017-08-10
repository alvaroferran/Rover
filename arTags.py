#!/usr/bin/env python

import math
import numpy as np
import cv2
import wheelsLib as wheels
import tagsLib as tags


def main():

    camRet = tags.cameraInit()
    capture, imgSize, target = camRet

    while True:
        tagCorners = tags.findTag(capture)

        if tagCorners is not None:
            tagCenter, tagArea = tags.processTagInfo(tagCorners)
            tagPercent = (tagArea * 100) / (imgSize[0] * imgSize[1])
            direction, speed = tags.calcDirSpeed(tagCenter, tagPercent, camRet)
            wheels.drive(direction, speed)

        # EXIT
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    tags.cameraStop(capture)


if __name__ == "__main__":
    main()
