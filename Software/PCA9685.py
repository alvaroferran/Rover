#!/usr/bin/python

import smbus
import time

PCA9685_ADDRESS = 0x40
PCA9685_FIRST = 0x06
PCA9685_ALL = 0xFA


def percent2value(percent):
    value = int(percent * 40.95)     # 0-100% -> 0-4095
    regH = (value & 0xF00) >> 8
    regL = value & 0xFF
    return (regL, regH)


def writePWM(channel, value):
    valL, valH = percent2value(value)
    vals = [0x00, 0x00, valL, valH]   # LedOnL, LedOnH, LedOffL, LedOffH
    bus.write_i2c_block_data(PCA9685_ADDRESS, PCA9685_FIRST+channel*4, vals)


def init():
    # Set SLEEP to 0 to start oscillator
    bus.write_byte_data(PCA9685_ADDRESS, 0x00, 0x01)
    time.sleep(0.001)
    # Set AutoIncrement to 1
    bus.write_byte_data(PCA9685_ADDRESS, 0x00, 0xA0)
    # Set OUTDRV and OUTNE0 to 1 in MODE2 register
    bus.write_byte_data(PCA9685_ADDRESS, 0x01, 0x05)
    time.sleep(0.001)
    # Turn all outputs to LOW
    off = [0x00, 0x00, 0x00, 0x10]
    bus.write_i2c_block_data(PCA9685_ADDRESS, PCA9685_ALL, off)


P0 = 14
P1 = 13
P2 = 12
P3 = 15
P4 = 0
P5 = 1
P6 = 6
P7 = 7

bus = smbus.SMBus(0)    # 0: /dev/i2c-0, 1: /dev/i2c-1
init()

valMin = 0
valMax = 100
steps = 20
delay = 0.5

while True:

    for speed in range(valMin, valMax, steps):
        writePWM(P4, speed)
        writePWM(P5, 0)
        time.sleep(delay)

    for speed in range(valMax, valMin, -steps):
        writePWM(P4, speed)
        writePWM(P5, 0)
        time.sleep(delay)

    for speed in range(valMin, valMax, steps):
        writePWM(P4, 0)
        writePWM(P5, speed)
        time.sleep(delay)

    for speed in range(valMax, valMin, -steps):
        writePWM(P4, 0)
        writePWM(P5, speed)
        time.sleep(delay)
