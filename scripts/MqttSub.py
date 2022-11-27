from MqttClient import *
import time

def onMessage(client, userData, msg):
  print(str(msg.payload.decode("utf-8")))

try:
    subMqtt = MqttClient("localhost",onMessage=onMessage)
    subMqtt.subscribe(topic="test")
    subMqtt.run()
    while True:
        pass
except KeyboardInterrupt:






