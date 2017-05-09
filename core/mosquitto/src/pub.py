import paho.mqtt.client as mqtt

mqttc = mqtt.Client("python_pub")
mqttc.connect("localhost", 1883)
mqttc.publish("test/1", "Hello, World!", 0)
mqttc.loop(2)  # timeout = 2s
