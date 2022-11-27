from MqttClient import *
import time

pubMqtt = MqttClient("localhost")

pubMqtt.run()

while True :
    time.sleep(1)
    pubMqtt.publish(topic="test" , msg="test")