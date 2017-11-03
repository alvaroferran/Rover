#!/usr/bin/python

import smbus
import time


def twos_complement(input_value, num_bits):
    mask = 2**(num_bits - 1)
    return -(input_value & mask) + (input_value & ~mask)


bus = smbus.SMBus(0)    # 0: /dev/i2c-0, 1: /dev/i2c-1
ADS1000_ADDRESS = 0x48  # IC address marking: BDO=0x48, BD1=0x49
ADS1000_OUTPUT = 0x00

while True:
    rawData = bus.read_i2c_block_data(ADS1000_ADDRESS, ADS1000_OUTPUT, 2)
    # From datasheet, 12bit ADC: 4 last bits of first byte and second byte
    adcH = rawData[0] & 15              # AND 0000 1111 -> take lower 4 bits
    adc = adcH << 8 | rawData[1]        # Create 12bit word
    adc = twos_complement(adc, 12)      # Find decimal equivalent
    voltage = (1.625-adc*3.25/2048)*2   # Calculate voltage from equation
                                        # (3V3 is actually 3.25 volts, YMMV)
    print('%.2f' % voltage)
    time.sleep(1)
