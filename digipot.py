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
spi.max_speed_hz = 10000
spi.mode = 0

def read_wiper():
    # read wiper setting
    msg = [0b00001111,0xFF]
    r = spi.xfer2(msg)
    print("answer")
    print(r)

# write wiper setting
msg = [0x00,0xFF]
spi.xfer2(msg)

read_wiper()

time.sleep(1);

msg = [0x00,0xA0]
spi.xfer2(msg)

read_wiper()

time.sleep(1);

msg = [0x00,0x00]
spi.xfer2(msg)

read_wiper()



msg = [0x00,0x00]
spi.xfer2(msg)
for i in range(0,255):
  msg = [0b00000100]
  spi.xfer2(msg)
  time.sleep(0.05)
  read_wiper()
  time.sleep(0.05)

