#!/usr/bin/env python


def map(vx, v1, v2, n1, n2):
    # v1 start of range, v2 end of range, vx the starting number in the range
    percentage = (vx - v1) / (v2 - v1)
    # n1 start of new range, n2 end of new range
    return (n2 - n1) * percentage + n1


def constrain(val, valMin, valMax):
    if val > valMax:
        return valMax
    if val < valMin:
        return valMin
    return val
