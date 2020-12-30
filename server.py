import os
from threading import  Thread
from flask import Flask, request,Response,jsonify
import time
from db.db import *



app = Flask(__name__)
@app.route('/')
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
    app.run("0.0.0.0",5000)

thread1 = Thread(target=run_server)

try:
    thread1.start()
    os.system("node mqtt_broker/broker.js")
except Exception as e:
    #pass
    print(e)

#thread1._stop()