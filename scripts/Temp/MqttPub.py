from MqttClient import *
from DataManager import *

""" # publisher

import time
import paho.mqtt.client as mqtt

ip = input("브로커의 IP 주소>>")

client = mqtt.Client()
client.connect(ip, 1883)
client.loop_start()

count = 0
while(True):
        message = input("문자메시지>>")
        if message == "exit" :
             break
        client.publish("letter", message, qos=0)
        print("sending %s" % message)
client.loop_stop()
client.disconnect()"""

def onMessage(client, userdata, msg):
  content = str(msg.payload.decode("utf-8"))
  print(content)
  if(content == 'request'):
        message = dataManager.readByJson()
        mqttClient.publish("json_response", message)
        print("sending %s" % message)

mqttClient = MqttClient(ip="localhost" , topic="json_request" ,onMessage=onMessage)
dataManager = DataManager()
mqttClient.run()

while(True):
        message = input("문자메시지>>")
        if message == "exit" :
             break

mqttClient.stop()