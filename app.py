import os
from threading import  Thread
from flask import Flask, render_template
import time
import socket
import signal
import sys
from db.db import *


app = Flask(__name__)

@app.route('/')
def signin():
    return render_template("signin.html")

@app.route('/index')
def index():
    return render_template("index.html")

@app.route('/home')
def home():
    return render_template("home.html")

@app.route("/about")
def about():
    return render_template("about.html")

def home():
    return "This is home page "

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

def run_server():
    global app
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    app.run("",5000)

thread1 = Thread(target=run_server)

def signal_handler(signal, frame):
    global thread1,app
    print(" * Terminate Flask server")
    sys.exit()

try:
   if __name__ == "__main__": 
      signal.signal(signal.SIGINT, signal_handler)
      thread1.start()
      os.system("node mqtt_broker/broker.js")
except  Exception as e:
     print(e)

