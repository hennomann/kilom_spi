#!/usr/bin/env python3


from high_level_tdc import *

print("enable_calib_pulser()")
enable_calib_pulser()

print("read_scaler(0)")
print(read_scaler(0))

print("scaler_rate(0,delay=0.1)")
print(scaler_rate(0,delay=0.1))

print("arm()")
arm()

print("read_tdc_chan(0)")
print(read_tdc_chan(0))

print("read_tot(0)")
print(read_tot(0))

print("disable_calib_pulser()")
disable_calib_pulser()
