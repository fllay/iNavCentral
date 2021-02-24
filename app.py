import os
from threading import  Thread
from flask import Flask, render_template, request, session, redirect, url_for, g
import time
import socket
import signal
import sys
from db.db import *
from db.Authenticate import *

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

global COOKIE_TIME_OUT
COOKIE_TIME_OUT = 60*60*24*7 #7 days

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

@app.route('/network')
def network():
    return render_template("network.html")

@app.route('/user')
def user():    
    return render_template("user.html", doc= get_list())

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']        
        add_new_user()
        return redirect(url_for('user'))

    return render_template("register.html")

@app.route('/datalogging')
def datalogging():
    return render_template("datalogging.html")

@app.route('/payout')
def payout():
    return render_template("payout.html")

@app.route('/carprocess')
def carprocess():
    return render_template("carprocess.html")

@app.route('/message')
def message():
    return render_template("message.html")

@app.route('/home')
def home():
    return render_template("home.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/queuing")
def queuing():
    return render_template("queuing.html")
   
@app.route("/sectionlist")
def sectionlist():
    return render_template("sectionlist.html")
   
@app.route("/sectioncolumn")
def sectioncolumn():
    return render_template("sectioncolumn.html")

@app.route("/car")
def car():
    return render_template("car.html")

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
      app.run(debug=True)  
      #thread1.start()
      os.system("node mqtt_broker/broker.js")      
except  Exception as e:
     print(e)


