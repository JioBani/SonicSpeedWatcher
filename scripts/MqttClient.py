import paho.mqtt.client as mqtt

def onConnect(client, userData, flag, rc):
    print("Connect with result code:"+ str(rc))

class MqttClient:

    def __init__(self, ip, onMessage = None):
        self.ip = ip
        self.client = mqtt.Client()
        self.client.on_connect = onConnect
        self.client.on_message = onMessage

    def onConnect(self,client, userData, flag, rc):
        print("Connect with result code:"+ str(rc))

    def subscribe(self,topic):
        self.client.subscribe(topic=topic,qos=0)

    def publish(self,topic,msg):
        self.client.publish(topic=topic,payload=msg,qos=0)

    def run(self):
        self.onConnect(self.ip , 1883)