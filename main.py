import pycom
import time
import machine
from LIS2HH12 import LIS2HH12
from pytrack import Pytrack
from pysense import Pysense
#from network import WLAN
from machine import I2C, Pin
import mpu6050

pycom.heartbeat(True)
#pycom.rgbled(0x0A0A08) # white

#wlan = WLAN(mode=WLAN.STA)
#wlan.connect(ssid='eduroam', auth=(WLAN.WPA2_ENT, 'viko', 'J9x4xbisFVQZ91Ebxqy6qgsh'), identity='myidentity')

#i2c = I2C(0, pins=('P8', 'P9'))     # create and use non-default PIN assignments (P10=SDA, P11=SCL)

i2c = I2C()
accelerometer = mpu6050.accel(i2c)
while True:
    time.sleep(1)
    vals = accelerometer.get_values()
    print(vals)