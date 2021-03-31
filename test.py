#!/usr/bin/env python3
import struct
import kilom_spi

# Open SPI device
device = kilom_spi.open()

rcmd=0x40
wcmd=0xC0
data = 0xbeef

kilom_spi.write(device,wcmd,data)

r=kilom_spi.read(device,rcmd)
print("0x ",end="")
for byte in r[1:]:
    print("{:02x} ".format(byte),end="")
print()
