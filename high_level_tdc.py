#!/usr/bin/env python3
#import spi2b4b
import spi2b4b
import struct

from time import sleep
import RPi.GPIO as GPIO


# this is the GPIO pin to select between flash access
# and register communication
# pulling it low means 
GPIO.setmode(GPIO.BCM)
GPIO.setup(2, GPIO.OUT)

GPIO.output(2,0)


HW_TRIG_GPIO = 16
GPIO.setup(HW_TRIG_GPIO, GPIO.IN)


rcmd=0x04
wcmd=0x14

# Open SPI device
device = spi2b4b.open();

coarse_bin = 1./(150e6)
fine_bin = coarse_bin/16.

def acquire(**kwargs):
  channels = kwargs.get("channels",range(0,8))
  trig_chan = kwargs.get("trig_chan",0)

  timeout = kwargs.get("timeout",1)

  # optional - ref_chan is trig_chan if not declared differently
  ref_chan  = kwargs.get("ref_chan",trig_chan)

  #"trigger" window before trigger
  window_L = kwargs.get("window_L",-1e-6)
  #"trigger" window after trigger
  window_R = kwargs.get("window_R",1e-6)

  clear_hw_trig()
  trigger_on_chan(trig_chan)
  arm()
  wait_for_trig(timeout=timeout)

  t_ref = read_tdc_chan(2*ref_chan)
  if (t_ref == None):
    print("got no trigger within timeout")
    return None

  #print("t_ref")
  #print(t_ref)

  for ch in channels:
    t1 = None
    pre_t1 = read_pre_tdc_chan(2*ch)

    # does pre_t1 fulfill the criteria?
    # if yes, make it the new t1
    if (pre_t1 != None) :
      ttemp = pre_t1 - t_ref
      if ( ttemp > window_L ):
        t1 = ttemp

    # t1 hasn't been found yet?, look in the post register
    if  (t1 == None) :
      post_t1     = read_tdc_chan(2*ch)
      if (post_t1 != None) :
        ttemp = post_t1 - t_ref
        if ( ttemp < window_R ):
          t1 = ttemp


    if (t1 != None):
      # we have a leading edge!
      # now lets find the trailing edge!
      t2 = None
      # only need to read pre-register when t1 is < 0
      if ( t1 <0 ):
        pre_t2 = read_pre_tdc_chan(2*ch+1)
        if (pre_t2 != None):
          ttemp = pre_t2 - t_ref
          if (( ttemp > window_L) and (ttemp > t1)):
            t2 = ttemp

      # haven't found t2 yet, check the post register
      if (t2 == None):
        post_t2     = read_tdc_chan(2*ch+1)
        if (post_t2 != None):
          ttemp = post_t2 - t_ref
          if (( ttemp < window_R) and (ttemp > t1)):
            t2 = ttemp
      
      tot = -1e-9
      if (t2 != None):
        tot = t2 - t1
        
      
      print("ch {:d}, t1 = {:9.2f} ns, tot = {:9.2f} ns".format(ch,t1*1e9,tot*1e9))





def get_trig_state():
  return GPIO.input(HW_TRIG_GPIO)

def wait_for_trig(**kwargs):
  timeout = int(1000*float(kwargs.get("timeout",1)))
  if (get_trig_state() == 0):
    GPIO.wait_for_edge(HW_TRIG_GPIO, GPIO.RISING,timeout=timeout)


def trigger_on_chan(ch):
  or_map = get_hw_trig_map()
  or_map |= 1<<ch
  set_hw_trig_map(or_map)

def get_hw_trig_map():
  return read_register(0x08,0x00)   

def clear_hw_trig():
  set_hw_trig_map(0)

def set_hw_trig_map(or_map):
  write_register(0x18,0x00,or_map)   

def disable_stretcher():
  spi2b4b.write(device,0x14,0x01,0x10)

def enable_stretcher():
  spi2b4b.write(device,0x14,0x01,0x00)


def write_register(cmd,addr,data):
  spi2b4b.write(device,cmd,addr,data)


def read_register(cmd,addr):
  return int.from_bytes(
          spi2b4b.read(device,cmd, addr ),
          signed=False, byteorder='big'
          )

def read_scaler(ch):

  r= int.from_bytes(
          spi2b4b.read(device,0x03, 0xFF&ch ),
          signed=False, byteorder='big'
          )
  ref_cnt = r>>20
  hit_cnt = (r & 0b11111111111111111111)
  return [ref_cnt, hit_cnt]

def scaler_rate(ch,**kwargs):
  delay = float(kwargs.get("delay",1))
  ref_cnt_a, cnt_a = read_scaler(ch)
  sleep(delay)
  ref_cnt_b, cnt_b = read_scaler(ch)
  net_cnt = (cnt_b - cnt_a)
  delay_cnt = (ref_cnt_b - ref_cnt_a)
  if(delay_cnt <0):
    delay_cnt += 2**12
  meas_delay = delay_cnt*873.81e-6
  if(net_cnt <0):
    net_cnt += 2**20
  
  return net_cnt/meas_delay

def enable_calib_pulser():
  spi2b4b.write(device,0x14,0x02,0x01)

def disable_calib_pulser():
  spi2b4b.write(device,0x14,0x02,0x00)

def arm():
  spi2b4b.write(device,0xa0,0x00,0x00)

def trigger():
  spi2b4b.write(device,0xb0,0x00,0x00)

def read_tdc_chan(ch):

  r= int.from_bytes(
          spi2b4b.read(device,0x02, 0xFF&ch ),
          signed=False, byteorder='big'
          )

  fine_cnt   = r & 0b1111
  check_bits = r & 0b11110000
  coarse_cnt = r>>8
  if( check_bits == 0 ):
    return coarse_cnt*coarse_bin - fine_cnt*fine_bin
  else:
    return None

def read_pre_tdc_chan(ch):

  r= int.from_bytes(
          spi2b4b.read(device,0x07, 0xFF&ch ),
          signed=False, byteorder='big'
          )

  fine_cnt   = r & 0b1111
  check_bits = r & 0b11110000
  coarse_cnt = r>>8
  if( check_bits == 0 ):
    return coarse_cnt*coarse_bin - fine_cnt*fine_bin
  else:
    return None


def read_fine_cnt(ch):
  r= int.from_bytes(
          spi2b4b.read(device,0x02, (0xFF&ch) ),
          signed=False, byteorder='big'
          )

  fine_cnt = r & 0b1111
  return fine_cnt



def read_t1(ch):
  t1 = read_tdc_chan(2*ch)
  return t1

def read_pre_t1(ch):
  t1 = read_pre_tdc_chan(2*ch)
  return t1

def read_t2(ch):
  t2 = read_tdc_chan(2*ch+1)
  return t2

def read_pre_t2(ch):
  t2 = read_pre_tdc_chan(2*ch+1)
  return t2

def read_tot(ch):
  t2 = read_tdc_chan(2*ch+1)
  t1 = read_tdc_chan(2*ch)
  if ((t2 != None) and (t1 != None) ):
    return t2 -t1
  return None

def read_pre_tot(ch):
  t2 = read_pre_tdc_chan(2*ch+1)
  t1 = read_pre_tdc_chan(2*ch)
  if ((t2 != None) and (t1 != None) ):
    return t2 -t1
  return None


#print(read_scaler(0))

#enable_calib_pulser()
#disable_calib_pulser()



#for i in range(0,16):
#  print(scaler_rate(i,delay=0.2))

#arm()
#sleep(0.01)
#print(read_tot(0))

