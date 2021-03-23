import paho.mqtt.client as mqtt
import time
from threading import Thread
import json 

def on_disconnect(client, userdata, rc):
    flag_connected = 0
    print("client disconnected")

def on_connect(self, client, userdata, rc):
    print(" * MQTT Connected.")
    self.subscribe("/AGV3/check")

class MQTTComm():
    def __init__(self):
        self.app =  mqtt.Client()
        self.host = "central"
        self.port = 1883
        self.app.on_connect = on_connect
        self.app.on_disconnect = on_disconnect
        self.app.on_message = self.on_message
        self.rcvMSG = ""

    def on_message(self,client, userdata,msg):
        message = msg.payload.decode("utf-8", "strict")
        self.rcvMSG = message
        print(self.rcvMSG)
  
    def connect(self):
        print(" * Connecting !")
        self.app.connect(host=self.host,port=self.port,keepalive=100)

    def start(self):
        self.connect()
        self.app.loop_start()

    def stop(self):
        self.app.loop_stop()

