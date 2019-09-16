#def checkposition(arg1, arg2)
import time
import numpy as np
import serial

ser = serial.Serial(
    "/dev/ttyAMA0",
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    writeTimeout=1,
    timeout=10,
    rtscts=False,
    dsrdtr=False,
    xonxoff=False)

ser.write('w'.encode()) 
time.sleep(1)
ser.write('o'.encode())
time.sleep(1)
distance=3
inc=int(distance/4)
du=distance-inc*4
print(inc)
for i in range(0,inc):
    ser.write('z'.encode())
    time.sleep(1)
time_run=(distance+inc+1)
print(time_run)
#ser.write('z'.encode())
#time.sleep(1)
#ser.write('z'.encode())
#time.sleep(1)
#ser.write('z'.encode())
#time.sleep(1)
#ser.write('z'.encode())
time.sleep(time_run)
#ser.write('x'.encode())
#time.sleep(1)
#ser.write('x'.encode())
#time.sleep(1)
#ser.write('x'.encode())
#time.sleep(1)
for i in range(0,inc):
    ser.write('x'.encode())
    time.sleep(1)
#ser.write('x'.encode())
if inc>=3:
    time.sleep(4*(inc-3))
else:
    time.sleep(4*inc)
    
if inc>=2:
    time.sleep(2)

    
ser.write('o'.encode())
time.sleep(du*4)
ser.write('s'.encode()) 