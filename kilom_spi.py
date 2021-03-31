# Python functions for SPI communication
# between Raspberry Pi (master) and KILOM module (slave)
# Henning Heggen, EE, GSI
# h.heggen@gsi.de
# Version 0.1

#!/usr/bin/env python3

import spidev
import struct

# Open SPI connection
def open():
    try:
        spi_device = spidev.SpiDev()
        spi_device.open(0,0)
        spi_device.max_speed_hz = 20000000
        spi_device.mode = 0
    except Exception as e:
        print("Failed to open SPI connection")
        print(e.message, e.args)
        return
    return spi_device


# Register write function accepting integers as arguments
def write(device, cmd, data):
    msg = [0x00,0x00,0x00,0x00,0x00]
    msg[0] = cmd
    data = struct.unpack('4B',struct.pack('>I',data))
    msg[1]=data[0]
    msg[2]=data[1]
    msg[3]=data[2]
    msg[4]=data[3]
    device.xfer2(msg)

# Register read function accepting integers as arguments
def read(device, cmd):
    msg = [0x00,0x00,0x00,0x00,0x00]
    msg[0] = cmd
    r = device.xfer2(msg)
    #print("0x ",end="")
    #for byte in r[1:]:
    #    print("{:02x} ".format(byte),end="")
    #print()
    return r


# Read scaler of channel <ch> (0...7)
def read_scaler(device, ch):
    msg = [0x00,0x00,0x00,0x00,0x00]
    msg[0] = cmd
    r = device.xfer2(msg)
    return r


# Register write function accepting strings as arguments
def str_write(device, cmd_str, data_str):
    msg = [0x00,0x00,0x00,0x00,0x00]
    msg[0] = int(cmd_str, 0)
    data = struct.unpack('4B',struct.pack('>I',int(data_str, 0)))
    msg[1]=data[0]
    msg[2]=data[1]
    msg[3]=data[2]
    msg[4]=data[3]
    device.xfer2(msg)

# Register read function accepting strings as arguments
def str_read(device, cmd_str):
    msg = [0x00,0x00,0x00,0x00,0x00]
    msg[0] = int(cmd_str, 0)
    r = device.xfer2(msg)
    #print("0x ",end="")
    #for byte in r[1:]:
    #    print("{:02x} ".format(byte),end="")
    #print()
    return r
