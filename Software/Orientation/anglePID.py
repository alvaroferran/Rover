#!/usr/bin/python
from BNO055 import BNO055
import subprocess
import sys
sys.path.append('/home/nanopi')
from NeoBoardClasses import DifferentialDrive
import time

sensor = BNO055(0x29)

motLA = 7
motLB = 6
motRA = 5
motRB = 4
minSpeed =12
maxSpeed = 100
wheels = DifferentialDrive(motLA, motLB, motRA, motRB, minSpeed, maxSpeed)

desiredAngle = 160

Kp = 22
Kd = 80
Ki = 0
currentAngle = 0.0
error = 0.0

try:
    time.sleep(0.100)
    iteration = 0
    delay = 0.010

    # Export data to create a response graph
    fileName = "data"
    fileOut = open(fileName, "w")

    while True :
        time.sleep(delay)
        # Read current angle
        lastAngle = currentAngle;
        sensor.readEul()
        currentAngle = sensor.euler['x']
        # print(currentAngle)
        # Error
        lastError = error
        error = desiredAngle - currentAngle
        margin = 1
        if abs(error) < margin:
            error = 0
        # Calculate average speed
        # Move all speed values one space to the left to make space for the newest one
        num = 5
        v = [0] * num
        for i in range(0,num):
            if i < num-1:
                v[i] = v[i+1]
        v[num-1] = error-lastError #  Add last speed
        vel=0.0
        # Average speed
        for i in range(0,num):
            vel = vel + v[i]
        vel /= num
        # I
        # if(abs(error)<10 && abs(error)>0.2)
        #     I+=error*Ki;
        # else
        I=0
        # Speed calculation
        direction = Kp*error + Kd*vel + I
        direction /= 1000.0
        if direction > 1.0:
            direction = 1.0
        if direction < -1.0:
            direction = -1.0
        print ("Angle: {:0.1f},  dir:{:0.2f}".format(currentAngle, direction))
        # Motor control
        wheels.drive(direction, 0, 1)
        # Write to file
        iteration += 1
        fileOut.write(str(delay*iteration) + ";" + str(currentAngle) + "\r\n")

finally:
    fileOut.close()
    wheels.drive(0, 0, 1)
