from flask import Flask, jsonify, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, emit
import json
import os
from control import Control
from emergency import Emergency

app = Flask(__name__)
socketio = SocketIO(app) 

status = {'room1Led': 0, 'room2Led': 0, 'room1Fan': 0, 'room2Fan': 0, 'emergency':0, 'maindoor': 0}
user = None

@app.route('/')
def index():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    else:
        return render_template('index.html', username = user)

@app.route('/data', methods = ['GET'] )
def data():
    return json.dumps(status)

@app.route('/livefeed', methods = ['GET'])
def livefeed():
    return "live feed"

@app.route('/login', methods=['POST', 'GET'])
def login():
    error = None
    global user
    if request.method == 'POST':    
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            session['logged_in'] = True
            user = request.form['username']
            return redirect(url_for('index'))
    return render_template('login.html', error=error)

@app.route("/logout")
def logout():
    session['logged_in'] = False
    return index()

@socketio.on('maindoor')
def maindoor(value):
    Control.maindoor(value)

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
    #print(status)
    print(virtualButtonStatus)
    status = json.dumps(virtualButtonStatus)
    print(status)
    status = json.loads(status)
    Control.change(status)
    print(status['room1Led'])
    emit('data',status, broadcast = True)
 
if __name__ == '__main__':
    Control.setup()
    app.secret_key = os.urandom(12)
    app.run(host = '0.0.0.0', debug=True)