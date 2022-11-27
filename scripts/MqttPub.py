from MqttClient import *
import time

pubMqtt = MqttClient("localhost")

pubMqtt.run()

while True :
    msg = input("메세지 입력")
    if(msg == 'exit') : break
    pubMqtt.publish(topic="test" , msg=msg)
    pubMqtt.run()