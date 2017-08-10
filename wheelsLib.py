#!/usr/bin/env python


def constrain(val, valMin, valMax):
    if val > valMax:
        return valMax
    if val < valMin:
        return valMin
    return val


def writeMotor(motor, value):
    minSpeed = 0
    maxSpeed = 1

    if motor == 1:
        channel1 = 0
        channel2 = 0
    elif motor == 2:
        channel1 = 0
        channel2 = 0

    # value = doubleMap(math.abs(value), 0,  1, minSpeed, maxSpeed)

    # if value>0:
        # pwmFunction(channel1, value)
        # pwmFunction(channel2, 0)
    # elif value<0:
        # pwmFunction(channel1, 0)
        # pwmFunction(channel2, value)
    # else:
        # pwmFunction(channel1, 0)
        # pwmFunction(channel2, 0)


def drive(steering, throttle, mode=0):

    if mode == 1 and throttle < 0:
        motATS = constrain(throttle * (1 - steering), -1, 1)
        motBTS = constrain(throttle * (1 + steering), -1, 1)
    else:
        motATS = constrain(throttle * (1 + steering), -1, 1)
        motBTS = constrain(throttle * (1 - steering), -1, 1)

    if mode == 1:
        motAS = + steering * (1 - fabs(throttle))
        motBS = - steering * (1 - fabs(throttle))
    else:
        motAS = 0
        motBS = 0

    motA = constrain(motATS + motAS, -1, 1)
    motB = constrain(motBTS + motBS, -1, 1)

    # writeMotor(1,motA)
    # writeMotor(2,motB)
    print("Motor1: %0.2f, Motor2: %0.2f" % (motA, motB))
