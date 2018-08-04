from time import sleep
import Adafruit_DHT
import threading

thread = threading.Thread()
thread_stop_event = threading.Event()

class Sensors(threading.Thread):
    def __init__(self):
        self.delay = 5
        super(Sensors, self).__init__()

    def main(self):
        while not thread_stop_event.isSet():
            humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.AM2302, 13)
            print ('Humidity is : {0:0.1f}'.format(humidity))
            print ('Temperature is : {0:0.1f}'.format(temperature))
            socketio.emit('sensors', {'humidity': humidity, 'temperature': temperature})
            sleep(self.delay)

    def run(self):
        self.main()