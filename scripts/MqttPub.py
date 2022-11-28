# publisher

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
client.disconnect()