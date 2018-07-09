from flask import Flask, jsonify, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, emit
import json
import os
from RPi.control import Control


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
    Control.change(status)
    print(status['room1Led'])
    emit('data',status, broadcast = True)
 
if __name__ == '__main__':
    Control.setup()
    app.secret_key = os.urandom(12)
    app.run(host = '0.0.0.0', debug=True)