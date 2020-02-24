import os
import machine
from network import WLAN
import pycom

uart = machine.UART(0, 115200)
os.dupterm(uart)

wl = WLAN()
wl.deinit()

pycom.heartbeat(False)

machine.main('main.py')
print('==========Starting main.py==========\n')