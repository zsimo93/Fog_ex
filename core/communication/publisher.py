import paho.mqtt.client as mqtt


class Publisher():

    def __init__(self, ip="localhost", name=""):
        self.mqttc = mqtt.Client(name)
        self.mqttc.connect(ip, 1883)

    def publish(self, topic, msg):
        self.mqttc.publish(topic, msg, 1)
        self.mqttc.loop(2)
