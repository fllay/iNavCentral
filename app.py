import os
from threading import  Thread
from flask import Flask, render_template, request, session, redirect, url_for, g
import time
import socket
import signal
import sys

from db.Authenticate import *

from mqtt_node.mqtt_node import MQTTComm

class User:
    def __init__(self, id ,username, password):
        self.id = id
        self.username = username
        self.password = password

    def __repr__(self):
        return f'<User: {self.username}>'

users = []
users.append(User(id=1,username='Admin',password='password'))
users.append(User(id=2,username='User',password='password'))


app = Flask(__name__)
app.secret_key = 'somesecretkkeyatsp'

@app.before_request
def before_request():
    if 'user_id' in session:
        user = [x for x in users if x.id == session['user_id']][0]
        g.user = user


@app.route('/signin',methods=['GET','POST'])
def signin():
    if request.method == 'POST':
        session.pop('user_id', None)
        username = request.form['username']
        password = request.form['password']

        user = [x for x in users if x.username == username][0]
        if user and user.password == password:
                session['user_id'] = user.id
                return redirect(url_for('index'))

        return redirect(url_for('signin'))
    return render_template("signin.html")

@app.route('/log_out')
def log_out():
    session.pop('user_id',None)
    return redirect(url_for('signin'))

@app.route('/index')
def index():
    return render_template("index.html")

@app.route('/home')
def home():
    return render_template("home.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route('/add/colection',  methods=['POST'])
def addNew():
    data_in = request.data
    data_in = data_in.decode("utf-8")
    print(data_in)
    data = {'Ok': '200'}
    return data,200

@app.route('/find',methods = ["POST"])
def find():
    return "This is find "

@app.route('/create')
def create():
    return "This is create"


def signal_handler(signal, frame):
    print(" * Terminate Flask server")       
    sys.exit()

mqttApp = MQTTComm()

try:
   if __name__ == "__main__":       
      signal.signal(signal.SIGINT, signal_handler)
      mqttApp.start()
      app.run(debug=True)  
          
except  Exception as e:
     print(e)


