from flask import Flask, jsonify, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, emit
import json
import os
from control import Control
from emergency import Emergency
from time import sleep
import Adafruit_DHT
from threading import Thread, Event
from automaticDoors import MainDoor
# import Adafruit_DHT, asyncio, time

app = Flask(__name__)
# app.config['SECRET_KEY'] = os.urandom(12)
# app.config['DEBUG'] = True
socketio = SocketIO(app)

status = {'room1Led': 0, 'room2Led': 0, 'room1Fan': 0, 'room2Fan': 0, 'emergency':0, 'maindoor': 0}
user = None

thread = Thread()
thread_stop_event = Event()

class Sensors(Thread):
    def __init__(self):
        self.delay = 5
        super(Sensors, self).__init__()

    def main(self):
        while not thread_stop_event.isSet():
            humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.AM2302, 13)
            # print ('Humidity is : {0:0.1f}'.format(humidity))
            # print ('Temperature is : {0:0.1f}'.format(temperature))
            socketio.emit('sensors', {'humidity': humidity, 'temperature': temperature})
            sleep(self.delay)

    def run(self):
        self.main()

@app.route('/')
def index():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
        return redirect(url_for('login'))
    else:
        return render_template('index.html', username = user)

@app.route('/data', methods = ['GET'] )
def data():
    return json.dumps(status)

@app.route('/livefeed', methods = ['GET'])
def livefeed():
    return render_template('livefeed.html', username = user)
    #redirect('http://localhost:8000')

@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    global user
    if request.method == 'POST':    
        user = request.form['username']
        password = request.form['password']
        if (user == 'admin' and password == 'admin'):
            session['logged_in'] = True
            return redirect(url_for('index'))
        elif user == 'amrinder' and password == 'amrinder':
            session['logged_in'] = True
            return redirect(url_for('index'))
        elif user == 'usman' and password == 'usman':
            session['logged_in'] = True
            return redirect(url_for('index'))
        else:   
            error = 'Invalid Credentials. Please try again.'
    return render_template('login.html', error=error)

@app.route("/logout")
def logout():
    session['logged_in'] = False
    return index()

@socketio.on('connect')
def connection():
    global thread 
    print('Client connected')
    if not thread.isAlive():
        thread = Sensors()
        thread.start()

@socketio.on('disconnect')
def disconnect():
    print("Client disconnected")

@socketio.on('maindoorLivefeed')
def mainDoorLiveFeed(value):
    global status
    maindoor(value)
    if value == 1:
        status['maindoor'] = 1
    else: status['maindoor'] = 0
    statusChange(status)

@socketio.on('maindoor')
def maindoor(value):
    Control.maindoor(value)
    # MainDoor.trigger(value)
    emit('mainDoorHandler', value, broadcast = True)
   
@socketio.on('emergency')
def emergency(flag):
    if(flag == 1):
        emit('emergencyON', broadcast = True)
        Emergency.email()
    else:
        emit('emergencyOFF', broadcast = True)
    
@socketio.on('statusChange')
def statusChange(virtualButtonStatus):
    global status
    status = json.dumps(virtualButtonStatus)
    status = json.loads(status)
    Control.change(status)
    emit('data',status, broadcast = True)

# async def sensors(x):
#     humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.AM2302, 26)
#     socketio.emit('sensors',humidity, temperature )
#     print("sensors")
#     await asyncio.sleep(x)

if __name__ == '__main__':
    Control.setup()
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(sensors(5))
    #call('python servotestclass.py'.split())
    #os.system('python servotestclass.py')
    #AutomaticDoors.controller()
    #subprocess.call("camera.py", shell = True)
    app.secret_key = os.urandom(12)
    app.run(host = '0.0.0.0', debug=True)
    