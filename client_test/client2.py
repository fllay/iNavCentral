import paho.mqtt.client as mqtt
import time
from threading import Thread
import json 

host = "192.168.1.44"
port = 1883
client = mqtt.Client()
flag_connected = 0

def on_disconnect(client, userdata, rc):
    global flag_connected
    flag_connected = 0
    print("client disconnected")

def on_connect(self, client, userdata, rc):
    global flag_connected
    print("MQTT Connected.")
    self.subscribe("TEST/MQTT")
    self.subscribe("newuser")

def on_message(client, userdata,msg):
    print(msg.payload.decode("utf-8", "strict"))

client.on_connect = on_connect
client.on_disconnect = on_disconnect
client.on_connect = on_connect
client.on_message = on_message
client.connect(host, port=1883, keepalive=60, bind_address="")

data = json.dumps({"name":"agv1","status":"load"})
while True:
      client.loop_start()
      client.publish("TEST/MQTT",data)
      time.sleep(1)

client.loop_stop()



      