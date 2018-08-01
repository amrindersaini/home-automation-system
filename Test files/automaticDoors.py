#!/usr/bin/env python

import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setup(16,GPIO.OUT)
GPIO.setup(25, GPIO.IN)
pwm = GPIO.PWM(16,50)
pwm.start(6)
try:
    while True:
        button_state = GPIO.input(25)
        if(button_state == 0):
            pwm.ChangeDutyCycle(6)
            sleep(1)
        elif(button_state == 1):
            pwm.ChangeDutyCycle(2.5)
            sleep(1)
        print("reached here")
except:
    #print("BC error")
    pwm.stop()
    GPIO.cleanup() 