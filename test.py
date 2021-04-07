#!/usr/bin/env python3
import struct
import spi2b4b

# Open SPI device
device = spi2b4b.open();

rcmd=0x04
wcmd=0x14
addr = 0
data = 0xdeadbeef

r=spi2b4b.read(device,rcmd,addr)
print("0x ",end="")
for byte in r[1:]:
    print("{:02x} ".format(byte),end="")
print()

spi2b4b.write(device,wcmd,addr,data)

r=spi2b4b.read(device,rcmd,addr)
print("0x ",end="")
for byte in r[1:]:
    print("{:02x} ".format(byte),end="")
print()
