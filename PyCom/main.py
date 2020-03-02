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
    time.sleep(2)
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
    print('Sending uplink message')
    pycom.rgbled(red)
    sock.send(payload)
    print('LoRa uplink complete')
    ack()


while True:
    x = mean(10, 'GyX')
    y = mean(10, 'GyY')
    z = mean(10, 'GyZ')
    print('x: ', x)
    print('y: ', y)
    if(x > 0 and y > 0):
        pycom.rgbled(red)
        lora_send('Detecting movement')
    else:
        pycom.rgbled(off)
        #time.sleep(5)
        #lora_send('No movement detection')
        

