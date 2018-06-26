from flask import Flask, jsonify, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, emit
import json
import os
import RPi.GPIO as GPIO
import time

app = Flask(__name__)
socketio = SocketIO(app)

status = {'user': None, 'room1Led': 0, 'room2Led': 0, 'room1Fan': 0, 'room2Fan': 0}

@app.route('/')
def index():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    else:
        return render_template('index.html')

@app.route('/data', methods = ['GET'] )
def data():
    return status

@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            session['logged_in'] = True
            #status['user']
            return redirect(url_for('index'))
    return render_template('login.html', error=error)

@app.route("/logout")
def logout():
    session['logged_in'] = False
    return index()

@socketio.on('statusChange')
def statusChange(virtualButtonStatus):
    global status
    #print(status)
    print(virtualButtonStatus)
    status = json.dumps(virtualButtonStatus)
    print(status)
    status = json.loads(status)
    control(status)
    print(status['room1Led'])
    emit('data',status, broadcast = True)


def setup():
    print("reached here")
    GPIO.setmode(GPIO.BCM)
    #GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)#Button to GPIO
    GPIO.setup(17, GPIO.OUT)  #LED to GPIO

def control(status):
    try:
        print("reached here")
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


if __name__ == '__main__':
    setup()
    app.secret_key = os.urandom(12)
    app.run(host = '0.0.0.0', debug=True)