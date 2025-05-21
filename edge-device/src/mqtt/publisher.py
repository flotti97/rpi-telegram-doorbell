import paho.mqtt.client as mqtt
import os

class MQTTPublisher:
    def __init__(self):
        self.client = mqtt.Client()
        self.client.connect(os.getenv("MQTT_BROKER", "localhost"), int(os.getenv("MQTT_PORT", 1883)))
        self.client.loop_start()

    def publish(self, topic, payload):
        self.client.publish(topic, payload)

# Shared instance for reuse
publisher = MQTTPublisher()
