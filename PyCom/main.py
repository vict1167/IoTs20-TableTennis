import pycom
import time
import machine
from LIS2HH12 import LIS2HH12
from pytrack import Pytrack
from pysense import Pysense

#from network import WLAN
from machine import I2C, Pin
import mpu6050

pycom.heartbeat(False)

i2c = I2C()
accelerometer = mpu6050.accel(i2c)



def mean(range, measure):
    data = 0
    for tmp in range(range):
        tmp = accelerometer.get_values()[measure]
        data += tmp
    return(data/range)




while True:
    x = mean(10, 'GyX')
    y = mean(10, 'GyY')
    z = mean(10, 'GyZ')
    print('x: ', x)
    print('y: ', y)
    if(x > 0 and y > 0):
        pycom.rgbled(0xFF0000)
    else:
        pycom.rgbled(0x000000)

