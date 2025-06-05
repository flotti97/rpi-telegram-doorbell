import paho.mqtt.client as mqtt
import os
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

class MQTTPublisher:
    def __init__(self):
        host = os.getenv("MQTT_BROKER", "localhost")
        port = int(os.getenv("MQTT_PORT", 1883))

        self.client = mqtt.Client()
        try:
            self.client.connect(host, port)
            print(f"[MQTT] Connected to {host}:{port}")
        except Exception as e:
            print(f"[MQTT] Failed to connect: {e}")

        self.client.loop_start()

    def publish(self, topic, payload):
        self.client.publish(topic, payload)

# Shared instance
publisher = MQTTPublisher()
