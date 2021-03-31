#!/usr/bin/env python3

import sys
import struct
import kilom_spi


# Open SPI device
device = kilom_spi.open()


# Parse arguments
args = sys.argv[1:]

# Check for number of arguments
if len(args) < 2:
    print("Error >>> too few arguments ({:})".format(len(args)))
    print("Usage: spicmd.py <r/w> <cmd byte> <if w: up to 4 data bytes (0x0-0xffffffff)>")
    exit(1)
if len(args) > 3:
    print("Error >>> too many arguments ({:})".format(len(args)))
    print("Usage: spicmd.py <r/w> <cmd byte> <if w: up to 4 data bytes (0x0-0xffffffff)>")
    exit(1)

# Evaluate operation parameter
op = args[0]
if op!="r" and op!="w":
    print("Error >>> invalid first argument (must be r or w)")
    print("Usage: spicmd.py <r/w> <cmd byte> <if w: up to 4 data bytes (0x0-0xffffffff)>")
    exit(1)
elif op=="w":
    if len(args) != 3:
        print("Error >>> wrong number of arguments (must be 3 for write)")
        print("Usage: spicmd.py <r/w> <cmd byte> <if w: up to 4 data bytes (0x0-0xffffffff)>")
        exit(1)
    else:
        data_str = args[2]
        
# Ealuate command parameter
cmd_str = args[1]

# Execute operation
if op=="w":
    kilom_spi.str_write(device, cmd_str, data_str)
else:
    r=kilom_spi.str_read(device, cmd_str)
    print("0x ",end="")
    for byte in r[1:]:
        print("{:02x} ".format(byte),end="")
    print()
