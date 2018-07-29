from time import sleep
import Adafruit_DHT
import sys

def readDHT22() :
    humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.AM2302, 4)
    return (humidity, temperature)

def main():
    while True:
        humidity, temperature = readDHT22()
        print ('Humidity is : {0:0.1f} %'.format(humidity))
        print ('Temperature is : {0:0.1f} C'.format(temperature))
        sleep(3)

if __name__ == '__main__':
    main()