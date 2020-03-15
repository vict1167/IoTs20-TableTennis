import machine
import pycom

pycom.heartbeat(False)

machine.main('main.py')
print('==========Starting main.py==========\n')
