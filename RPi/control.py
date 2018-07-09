import RPi.GPIO as GPIO
import time

class Control():
    def __init__(self, status):
        self.status = status;

    def setup():
        GPIO.setmode(GPIO.BCM)
        #GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)#Button to GPIO
        GPIO.setup(17, GPIO.OUT)  #LED to GPIO
        print("Setup done")

    def change(status):
        try:
            print("reached here")
            print(status['room1Led'])
            if status['room1Led'] == 1:
                GPIO.output(17, True)
                print("led on")
                time.sleep(0.2)
            elif status['room1Led'] == 0:
                print("led off")
                GPIO.output(17, False)
        except:
            print("GPIO cleanup")
            GPIO.cleanup()
