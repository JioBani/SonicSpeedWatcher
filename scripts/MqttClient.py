import paho.mqtt.client as mqtt

class MqttClient:

    def __init__(self, ip,topic,onMessage = None):
        self.ip = ip
        self.client = mqtt.Client()
        self.client.on_connect = self.onConnect
        self.client.on_message = onMessage
        self.topic = topic

    def onConnect(self,client, userData, flag, rc):
        print("Connect with result code:"+ str(rc))
        self.subscribe(self.topic)

    def subscribe(self,topic):
        self.client.subscribe(topic=topic,qos=0)

    def publish(self,topic,msg):
        self.client.publish(topic=topic,payload=msg,qos=0)

    def run(self):
        self.client.connect(self.ip , 1883)
        self.client.loop_start()

    def stop(self):
        self.client.loop_stop()
        self.client.disconnect()