#!/usr/bin/env python3

# spitest.py
# A brief demonstration of the Raspberry Pi SPI interface, using the Sparkfun
# Pi Wedge breakout board and a SparkFun Serial 7 Segment display:
# https://www.sparkfun.com/products/11629

import time
import spidev

# We only have SPI bus 0 available to us on the Pi
bus = 0

#Device is the chip select pin. Set to 0 or 1, depending on the connections
device = 0

# Enable SPI
spi = spidev.SpiDev()

# Open a connection to a specific bus and device (chip select pin)
spi.open(bus, device)

# Set SPI speed and mode
#spi.max_speed_hz = 500000
spi.max_speed_hz = 30000000
spi.mode = 0

def read_wiper():
    # read wiper setting
    msg = [0x40,0x00,0x00,0x00, 0x00]
    #print(msg)
    r = spi.xfer2(msg)
    print("answer")
    for byte in r[1:]:
        print("0x{:02x} ".format(byte),end="")
    print()

# write wiper setting
read_wiper()
