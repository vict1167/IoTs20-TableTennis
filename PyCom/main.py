import pycom
import time
import machine
from LIS2HH12 import LIS2HH12
from pytrack import Pytrack
from pysense import Pysense
from network import LoRa
import ubinascii
import binascii
import socket
import struct
import math
from machine import I2C, Pin
import mpu6050

# Initialize LoRaWAN radio
lora = LoRa(mode=LoRa.LORAWAN, region=LoRa.EU868)

# Colors
off = 0x000000
red = 0xff0000
green = 0x00ff00
blue = 0x0000ff

# Set network keys
dev_eui = binascii.unhexlify('70B3D54999A506C5')
app_eui = binascii.unhexlify('70B3D57ED002B1D1')
app_key = binascii.unhexlify('E5095A715F2C51C732AEFBEA1DE40095')

# Join the network
lora.join(activation=LoRa.OTAA, auth=(dev_eui, app_eui, app_key), timeout=0)
pycom.rgbled(red)

# Loop until joined
while not lora.has_joined():
    print('Not joined yet...')
    pycom.rgbled(off)
    time.sleep(0.1)
    pycom.rgbled(red)
    time.sleep(1)
print('Joined')
pycom.rgbled(blue)

sock = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
sock.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)
sock.setblocking(True)


# Setting up the accelerometer
i2c = I2C()
accelerometer = mpu6050.accel(i2c)


def mean(range, measure):
    data = 0
    for tmp in range(range):
        tmp = accelerometer.get_values()[measure]
        data += tmp
    return(data/range)

def ack():
    for i in range(3):
        pycom.rgbled(green)
        time.sleep_ms(100)
        pycom.rgbled(0)
        time.sleep_ms(100)


def lora_send(payload):
    print('Sending uplink message: ', payload)
    pycom.rgbled(red)
    a = sock.send(payload)
    print('LoRa uplink complete')
    ack()

# def ensuring_movement():
#     print('Ensuring movement')
#     x_old = mean(10, 'GyX')
#     y_old = mean(10, 'GyY')
#     z_old = mean(10, 'GyZ')

#     x_new = mean(10, 'GyX')
#     y_new = mean(10, 'GyY')
#     z_new = mean(10, 'GyZ')

#     if(math.abs(x_old - x_new) > 10 and math.abs(y_old - y_new) > 10):
#         lora_send(' ')
#         print('Confirmed movement')
#     else:
#         time.sleep(5)

def detection():
    x = mean(10, 'GyX')
    y = mean(10, 'GyY')
    z_new = mean(10, 'GyZ')
    time.sleep(1)
    z_old = mean(10, 'GyZ')
    print("new: ", z_new, "- old: ", z_old)
    if(abs(z_old - z_new) > 5):
        pycom.rgbled(green)
        print('Movement Detected ensuring detection...')
        lora_send("x:" + str(x) + ", y:" + str(y) + ", z:" + str(z_new))
    else:
        pycom.rgbled(off)
        time.sleep(5)
        #lora_send('No movement detection')

while True:
    detection()
    time.sleep(1)
    pycom.rgbled(off)
