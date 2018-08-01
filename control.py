import RPi.GPIO as GPIO
from emergency import Emergency

import time 

class Control():
    def __init__(self, status):
        self.status = status

    def setup():
        GPIO.setmode(GPIO.BCM)
        #GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)#Button to GPIO
        GPIO.setup(17, GPIO.OUT)  #Room1Led 
        GPIO.setup(27, GPIO.OUT)  #Room2Led
        GPIO.setup(23, GPIO.OUT)  #Room1Fan
        GPIO.setup(24, GPIO.OUT)  #Room2Fan
        GPIO.setup(26, GPIO.OUT) #Main door lock
        print("Setup done")

    def maindoor(value):
        print("Main door triggered: ")
        print(value)
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(26, GPIO.OUT) #Main door lock
        pwm = GPIO.PWM(26,50)
        pwm.start(6)
        try:
            if(value == 0):
                pwm.ChangeDutyCycle(6)
                time.sleep(1)
            elif(value == 1):
                pwm.ChangeDutyCycle(2.5)
                time.sleep(1)
            print("reached here")
        except:
            print("BC error")
            pwm.stop()
            GPIO.cleanup() 
        
    def emergency(value):
        Emergency.email(value)
        print("Emergency: ")
        print(value)

    def change(status):
        try:
            if status['room1Led'] == 1:
                GPIO.output(17, True)
                time.sleep(0.2)
            else:
                GPIO.output(17, False)
            if status['room2Led'] == 1:
                GPIO.output(27, True)
                time.sleep(0.2)
            else:
                GPIO.output(27, False)
            if status['room1Fan'] == 1:
                GPIO.output(23, True)
                time.sleep(0.2)
            else:
                GPIO.output(23, False)
            if status['room2Fan'] == 1:
                GPIO.output(24, True)
                time.sleep(0.2)
            else:
                GPIO.output(24, False)
        except KeyboardInterrupt:
            print("GPIO cleanup")
            GPIO.cleanup()
        

    