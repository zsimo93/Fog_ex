import mqtt, json


class Subscriber():

    def __init__(self, name, topic):
        self.name = name
        self.topic = topic

    def run(self, ip):

        def on_connect(client, userdata, flags, rc):
            print("Connected with result code " + str(rc))

            client.connect(self.topic)

        def on_message(client, userdata, msg):
            data = json.loads(msg.payload)
            type = data.pop('type')

            if type == "deploy":
                pass
            else:  # execute
                pass

        self.client = mqtt.Client(self.name)
        self.client.on_connect = on_connect
        self.client.on_message = on_message

        self.client.connect(ip, 1883, 60)

        self.client.start_loop()
