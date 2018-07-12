#!/usr/bin/python

import sys
import time
sys.path.append('/home/nanopi')
from NeoBoardClasses import DifferentialDrive, ADS1000
from BNO055 import BNO055
from Camera import Camera


class Rover:

    """
    High-level class to control the rover
    """

    def __init__(self):
        motLA = 7
        motLB = 6
        motRA = 5
        motRB = 4
        minSpeed = 11
        maxSpeed = 100
        self.wheels = DifferentialDrive(motLA, motLB, motRA, motRB, minSpeed,
                                        maxSpeed)
        self.imu = BNO055()
        self.battery = ADS1000()
        self.cam = Camera()

    def turnDegrees(self, degrees):
        """
        Turn rover X degrees left or right. Accepts angles between [-180 and
        180]
        """
        # Limit degrees to [-180:180]
        degrees = constrain(degrees, -180.0, 180.0)
        # Get current orientation
        time.sleep(0.1)     # Allow the IMU to get a first value
        self.imu.readEul()
        initPos = self.imu.euler['x']
        # Convert degrees to absolute reference frame
        degrees += initPos
        # Go to set angle
        self.__anglePID(degrees)

    def setAngle(self, degrees):
        """
        Turn rover to absolute orientation X. Accepts angles between [0 and
        360]
        """
        # Limit degrees to [0:360]
        degrees = constrain(degrees, 0.0, 360.0)
        # Go to set angle
        self.__anglePID(degrees)

    def getBattery(self):
        """
        Get rover's battery level. Returns a tuple containing (voltage,
        percentage)
        """
        return self.battery.readBattery()

    def drive(self, steering, throttle, mode=0):
        """
        Guide the rover with a speed and direction.
        """
        self.wheels.drive(steering, throttle, mode)

    def goToTag(self):
        """
        Find the largest AR tag and go towards it
        """
        percentMax = 3
        # speedStraightMax = 0.15
        speedStraightMax = 0.18
        speedTurnMax = 0.1
        percent = 0
        # Keep going until the tag is close enough
        self.cam.startCamera()
        while percent < percentMax:
            speed, direction, percent = (0, 0, 0)
            tagInfo = self.cam.detectTag()
            if tagInfo is not None:
                center, area = tagInfo
                print("Center area {} {}".format(center, area))

                percent = (area * 100) / (self.cam.width * self.cam.height)
                # Target window width
                windowScale = 0.1
                targetMin = self.cam.width/2 - int(self.cam.width*windowScale)
                targetMax = self.cam.width/2 + int(self.cam.width*windowScale)
                speed = map(percent, 0, percentMax, speedStraightMax, 0)
                if center[0] < targetMin:
                    direction = map(center[0], 0, targetMin, -speedTurnMax, 0)
                elif center[0] > targetMax:
                    direction = map(center[0], targetMax, self.cam.width, 0,
                                    speedTurnMax)
                else:
                    direction = 0
            print("Dir: {}  Speed: {}  %: {}".format(-direction, speed,
                  percent))
            self.wheels.drive(-direction, speed)
        # Send stop signal once arrived
        self.wheels.drive(0, 0)
        self.cam.stopCamera()

    def __anglePID(self, desiredAngle):
        """
        PID algorithm to take the rover to the specified orientation
        """
        Kp = 4.0
        Kd = 70.0
        Ki = 0.1
        delay = 0.01     # Angle updated at 100Hz
        margin = 0.2
        errorStartI = 3.0
        error = 0.0
        I = 0
        while True:
            time.sleep(delay)
            # Read current angle
            self.imu.readEul()
            currentAngle = self.imu.euler['x']
            # Convert to (-180,180]
            if currentAngle > 180:
                currentAngle -= 360
            # Error
            lastError = error
            error = desiredAngle - currentAngle
            if error > 180.0:
                error -= 360.0
            # Calculate average speed
            # Move all speed values one space to the left to make space for the
            # newest one
            num = 5
            v = [0] * num
            for i in range(0, num):
                if i < num-1:
                    v[i] = v[i+1]
            v[num-1] = error-lastError  # Add last speed
            vel = 0.0
            # Average speed
            for i in range(0, num):
                vel = vel + v[i]
            vel /= num
            # I
            if abs(error) < errorStartI and abs(error) > margin:
                I += error*Ki
            else:
                I = 0
            # Speed calculation
            speed = Kp*error + Kd*vel + I
            speed /= 100.0
            if speed > 1.0:
                speed = 1.0
            if speed < -1.0:
                speed = -1.0
            # Motor control
            self.wheels.drive(speed, 0, 1)
            if abs(error) < margin:
                break
        # Send stop signal to PCA driver
        self.wheels.drive(0, 0, 1)


def constrain(value, minVal, maxVal):
    if value < minVal:
        value = minVal
    if value > maxVal:
        value = maxVal
    return value


def map(vx, v1, v2, n1, n2):
    # v1 start of range, v2 end of range, vx the starting number in the range
    percentage = (vx - v1) / (v2 - v1)
    # n1 start of new range, n2 end of new range
    return (n2 - n1) * percentage + n1
