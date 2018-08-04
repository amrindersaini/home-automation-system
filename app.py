from flask import Flask, jsonify, render_template, request, redirect, url_for, session
from flask_login import logout_user, login_user, current_user, UserMixin, LoginManager, login_required
from flask_socketio import SocketIO, emit
from flask_wtf import form, FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import Email, Length, InputRequired
from flask_mongoengine import MongoEngine, Document
from werkzeug.security import check_password_hash , generate_password_hash
import json, urllib, os,  Adafruit_DHT
from control import Control
from emergency import Emergency
from time import sleep
from threading import Thread, Event
# import Adafruit_DHT, asyncio, time

app = Flask(__name__)

app.config['MONGODB_SETTINGS'] = {
    'db': 'userinfo ,',
    'host': 'mongodb://amrinder:amrinder76@ds263161.mlab.com:63161/userinfo',
    'connect' : False
}

db = MongoEngine(app)
app.config['SECRET_KEY'] = '<---YOUR_SECRET_FORM_KEY--->'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
# app.config['SECRET_KEY'] = os.urandom(12)
# app.config['DEBUG'] = True

socketio = SocketIO(app)

status = {'room1Led': 0, 'room2Led': 0, 'room1Fan': 0, 'room2Fan': 0, 'emergency':0, 'maindoor': 0}

thread = Thread()
thread_stop_event = Event()

class User(UserMixin, db.Document):
    meta = {'collection': 'user'}
    username = db.StringField(max_length=30)
    password = db.StringField()

@login_manager.user_loader
def load_user(user_id):
    return User.objects(pk=user_id).first()

class RegForm(FlaskForm):
    username = StringField('username',  validators=[InputRequired(), Length(max=30)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=4, max=20)])
    key = StringField('key', validators=[InputRequired()])

class LogForm(FlaskForm):
    username = StringField('username',  validators=[InputRequired(), Length(max=30)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=4, max=20)])

class Sensors(Thread):
    def __init__(self):
        self.delay = 2
        super(Sensors, self).__init__()

    def main(self):
        while not thread_stop_event.isSet():
            humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.AM2302, 13)
            socketio.emit('sensors', {'humidity': humidity, 'temperature': temperature})
            sleep(self.delay)

    def run(self):
        self.main()

@app.route('/')
def dashboard():
    if current_user.is_authenticated == True:
        return redirect(url_for('index'))
    else:
        return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegForm()
    if request.method == 'POST':
        if form.validate():
            if(form.key.data == 'TPJ655'):
                existing_user = User.objects(username=form.username.data).first()
                if existing_user is None:
                    hashpass = generate_password_hash(form.password.data, method='sha256')
                    hey = User(form.username.data,hashpass).save()
                    login_user(hey)
                    return redirect(url_for('index'))
            else:
                error = 'Invalid key. Please enter valid registration key and try again.'
                return render_template('register.html', form = form , error = error) 
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated == True:
        return redirect(url_for('index'))
    form = LogForm()
    if request.method == 'POST':
        if form.validate():
            check_user = User.objects(username=form.username.data).first()
            if check_user:
                if check_password_hash(check_user['password'], form.password.data):
                    login_user(check_user)
                    return redirect(url_for('index'))
            else: 
                error = 'Invalid Credentials. Please try again.'
                return render_template('login.html', form = form , error = error)
    return render_template('login.html', form=form)

@app.route('/index')
@login_required
def index():
    return render_template('index.html', username = current_user.username)

@app.route('/data', methods = ['GET'] )
@login_required
def data():
    return json.dumps(status)

@app.route('/livefeed', methods = ['GET'])
@login_required
def livefeed():
    # global status
    # emit('mainDoorLiveFeed', status['maindoor'], broadcast = True)
    return render_template('livefeed.html', username = current_user.username)

# @app.route('/status', methods = ['GET'] )
# @login_required
# def status():
#     return json.dumps(status['maindoor'])

@app.route("/logout", methods = ['GET'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

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
    emit('mainDoorHandler', value, broadcast = True)
   
@socketio.on('emergency')
def emergency(flag):
    if(flag == 1):
        emit('emergencyON', broadcast = True)
        humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.AM2302, 13)
        Emergency.email(current_user.username, temperature, humidity)
        Emergency.email(current_user.username)
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
    #app.secret_key = os.urandom(12)
    app.run(host = '0.0.0.0', debug=True)
    