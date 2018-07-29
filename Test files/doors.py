import RPi.GPIO as GPIO
from time import sleep

class Doors():
    def __call__(self):
        self.setup()

    def setup(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(12,GPIO.OUT)
        GPIO.setup(20, GPIO.IN)
        self.pwm = GPIO.PWM(12,50)
        self.pwm.start(0)
        self.controller()

    def SetAngle(angle):
        duty = angle / 18 + 2
        GPIO.output(12,True)
        self.pwm.ChangeDutyCycle(duty)
        sleep(1)
        GPIO.output(12,False)
        self.pwm.ChangeDutyCycle(0) 

    def change(self, button_state):
        if button_state == 0:
            self.SetAngle(0)
        elif button_state == 1:
            self.SetAngle(85)    

    def controller(self):
        last_button_state = 1
        try:
            while True:
                button_state = GPIO.input(20)
                print(button_state)
                if button_state != last_button_state:
                    print("im here")
                    self.change(button_state)
                    print("reached here")
                    #sleep(2.0)
                last_button_state = button_state
        except:
            print("BC error")
            self.pwm.stop()
            GPIO.cleanup()  

obj = Doors()
obj()