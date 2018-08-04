#!/usr/bin/env python

import RPi.GPIO as GPIO
from time import sleep

class MainDoor():
    def trigger(button_state):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(16,GPIO.OUT)
        pwm = GPIO.PWM(16,50)
        pwm.start(0)
        try:
            change(button_state, pwm)
            #print("reached here")
            sleep(2.0)
        except:
            #print("BC error")
            pwm.stop()
            GPIO.cleanup() 
        
    def SetAngle(angle, pwm):
        duty = angle / 18 + 2
        GPIO.output(16,True)
        pwm.ChangeDutyCycle(duty)
        sleep(1)
        GPIO.output(16,False)
        pwm.ChangeDutyCycle(0) 

    def change(self,button_state, pwm):
        if button_state == 0:
            self.SetAngle(0, pwm)
        elif button_state == 1:
            self.SetAngle(45, pwm)    