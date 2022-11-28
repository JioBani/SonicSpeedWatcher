# subscriber

import paho.mqtt.client as mqtt

def on_A(client, userdata, flag, rc):
        print("Connect with result code:"+ str(rc))
        client.subscribe("letter", qos = 0)

def on_B(client, userdata, msg):
        print(str(msg.payload.decode("utf-8")))
        # print(str(msg.payload))

ip = input("브로커의 IP 주소>>")

client = mqtt.Client()
client.on_connect = on_A
client.on_message = on_B
client.connect(ip, 1883)

client.loop_forever()
