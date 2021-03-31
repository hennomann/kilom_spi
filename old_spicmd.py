#!/usr/bin/env python3

import sys
import time
import spidev
import struct

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
spi.max_speed_hz = 20000000
spi.mode = 0

# Prepare transfer data array
msg = [0x00,0x00,0x00,0x00,0x00]

# Parse arguments
args = sys.argv[1:]

# Check for number of arguments
if len(args) < 2:
    print("Error >>> too few arguments ({:})".format(len(args)))
    print("Usage: kilom_spi.py <r/w> <cmd byte> <if w: up to 4 data bytes (0x0-0xffffffff)>")
    exit(1)
if len(args) > 3:
    print("Error >>> too many arguments ({:})".format(len(args)))
    print("Usage: kilom_spi.py <r/w> <cmd byte> <if w: up to 4 data bytes (0x0-0xffffffff)>")
    exit(1)

# Evaluate operation parameter
op = args[0]
if op!="r" and op!="w":
    print("Error >>> invalid first argument (must be r or w)")
    print("Usage: kilom_spi.py <r/w> <cmd byte> <if w: up to 4 data bytes (0x0-0xffffffff)>")
    exit(1)
elif op=="w":
    if len(args) != 3:
        print("Error >>> wrong number of arguments (must be 3 for write)")
        print("Usage: kilom_spi.py <r/w> <cmd byte> <if w: up to 4 data bytes (0x0-0xffffffff)>")
        exit(1)
    else:
        data_str = args[2]
        
# Ealuate command parameter
cmd_str = args[1]
cmd = int(cmd_str, 0)
if cmd > 255:
    print("Error >>> cmd value out of range (1 byte max)")
    print("Usage: kilom_spi.py <r/w> <cmd byte> <if w: up to 4 data bytes (0x0-0xffffffff)>")
    exit(1)
msg[0]=cmd

# Parse data argument for write command
if op=="w":
    data = struct.unpack('4B',struct.pack('>I',int(data_str, 0)))
    msg[1]=data[0]
    msg[2]=data[1]
    msg[3]=data[2]
    msg[4]=data[3]

def spi_write():
    spi.xfer2(msg)
        
def spi_read():
    # read wiper setting
    #msg = [0x30,0x00,0x00,0x00,0x10]
    #print(msg)
    r = spi.xfer2(msg)
    #print("answer")
    #print(r)
    for byte in r[1:]:
        print("0x{:02x} ".format(byte),end="")
    print()

if op=="w":
    spi_write();
else:
    spi_read();

