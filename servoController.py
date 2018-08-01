#!/usr/bin/env python

import RPi.GPIO as GPIO
from time import sleep

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(12,GPIO.OUT)
    GPIO.setup(20, GPIO.IN)
    
def SetAngle(angle):
    duty = angle / 18 + 2
    GPIO.output(12,True)
    pwm.ChangeDutyCycle(duty)
    sleep(1)
    GPIO.output(12,False)
    pwm.ChangeDutyCycle(0) 

def change(button_state):
    if button_state == 0:
        SetAngle(0)
    elif button_state == 1:
        SetAngle(115)    

def controller():
    last_button_state = 1
    try:
        while True:
            button_state = GPIO.input(20)
            #print(button_state)
            if button_state != last_button_state:
                change(button_state)
                #print("reached here")
                sleep(2.0)
            last_button_state = button_state
    except:
        #print("BC error")
        pwm.stop()
        GPIO.cleanup()  

if __name__ == '__main__':
    setup()
    pwm = GPIO.PWM(12,50)
    pwm.start(0)
    controller()
