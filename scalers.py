#!/usr/bin/python

import sys
from subprocess import call, Popen, PIPE
from time import sleep
import numpy as np
#import kilom_spi

integration_time = 0.01

t0_arr = np.zeros(8, dtype=int)
val0_arr = np.zeros(8, dtype=int)
t1_arr = np.zeros(8, dtype=int)
val1_arr = np.zeros(8, dtype=int)
rates = np.zeros(8, dtype=int)

# read all scalers for first time
for i in range(8):
    data = Popen(["kilom_spi.py", "r", "0x30"], stdout=PIPE).communicate()[0]
    t_h = data[:-7]
    val_h = "0x{0}".format(data[-7:])
    t0_arr[i] = int(t_h, 0)
    val0_arr[i] = int(val_h, 0)

# wait for duration of integration_time (set at top of program)
sleep(integration_time)

# read all scalers for second time
for i in range(8):
    regaddr = "0x201{0:0{1}X}".format(i*4,3)
    data = Popen(["gosipcmd", "-r", "-x", "{0}".format(sfp), "{0}".format(dev), "{0}".format(regaddr)], stdout=PIPE).communicate()[0]
    t_h = data[:-7]
    val_h = "0x{0}".format(data[-7:])
    t1_arr[i] = int(t_h, 0)
    val1_arr[i] = int(val_h, 0)

# calculate rates from counter value differences (val0, val1) and time reference counter difference (t0, t1)
for i in range(8):
    t0 = t0_arr[i]
    t1 = t1_arr[i]
    val0 = val0_arr[i]
    val1 = val1_arr[i]

    if t1 >= t0:
        dt = t1-t0
    else:
        dt = t1-t0+4095
        
    dts = dt*0.0005
    
    if val1 >= val0:
        counts = val1-val0
    else:
        counts = val1-val0+1048575

    if dts > 0:
        rate = counts / dts
    else:
        rate = 599999999
        
    rates[i] = int(round(rate))

    j=i+1
    # print rates in formatted way
    if j%8==0:
        print "#{8}\t{0:12}{1:12}{2:12}{3:12}{4:12}{5:12}{6:12}{7:12}".format(rates[i-7],rates[i-6],rates[i-5],rates[i-4],rates[i-3],rates[i-2],rates[i-1],rates[i],i-7)
