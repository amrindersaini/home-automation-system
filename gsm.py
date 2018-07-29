from __future__ import print_function
import time
from time import sleep
import serial

phone = serial.Serial("/dev/ttyUSB0", 115200, timeout=10)
recipient = "4168457945"

def emergency():
    message = "Current Temperature =>" + temperature
    message1 = "Current Humidity =>" + humidity
    phone.write(b'AT+CMGS="' + recipient.encode() + b'"\r')
    print ("Emergency: SMS is sending")
    time.sleep(1)
    phone.write(message.encode() + b"\r")
    phone.write(message1.encode() + b"\r")
    phone.write(message2.encode() + b"\r")
    phone.write(message3.encode() + b"\r")
    time.sleep(1)
    phone.write(bytes([26]))
