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
yellow = 0xffff00
green = 0x00ff00
pink = 0xff00ff
blue = 0x0000ff

# Set network keys
dev_eui = binascii.unhexlify('70B3D54999A506C5')
app_eui = binascii.unhexlify('70B3D57ED002B1D1')
app_key = binascii.unhexlify('E5095A715F2C51C732AEFBEA1DE40095')

# Setting up the accelerometer
i2c = I2C()
accelerometer = mpu6050.accel(i2c)

# Base value
mean = 19.75
standard_deviation = 13.3

def calibrate(range):
    data = []
    deviationData = []
    for x in range(range):
        data.append(accelerometer.get_values()['GyY'])

    mean = sum(data)/len(data)

    for y in data:
        deviationData.append(math.pow(y-mean,2))

    standard_deviation = math.sqrt(sum(deviationData)/len(deviationData))
    print(standard_deviation)

calibrate(10000)


def data(range, measure):
    pycom.rgbled(yellow)
    time.sleep(0.5)
    pycom.rgbled(off)
    data =[]
    for tmp in range(range):
        tmp = accelerometer.get_values()[measure] 
        if(abs(tmp-mean) > 3*standard_deviation):
            data.append(tmp)
    pycom.rgbled(yellow)
    time.sleep(0.5)
    pycom.rgbled(off)
    return(data)

def ack():
    for i in range(3):
        pycom.rgbled(green)
        time.sleep_ms(100)
        pycom.rgbled(0)
        time.sleep_ms(100)

def lora_send(payload):
    print('Sending uplink message: ', payload)
    pycom.rgbled(pink)
    a = sock.send(payload)
    print('LoRa uplink complete')
    ack()

while True:
    
    if(lora.has_joined()):
        n = len(data(10000, 'GyY'))
        
        if(n > 150):
            #ON
            lora_send("1" + "," + str(n))
            time.sleep(60)
        else:
            #OFF
            lora_send("0" + "," + str(n))
            time.sleep(60)
    else:
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
        pycom.rgbled(off)

        sock = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
        sock.setsockopt(socket.SOL_LORA, socket.SO_DR, 5)
        sock.setblocking(True)

