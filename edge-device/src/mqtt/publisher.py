<<<<<<< HEAD
import paho.mqtt.client as mqtt
import os
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

class MQTTPublisher:
    def __init__(self):
        self.host = os.getenv("MQTT_BROKER", "localhost")
        self.port = int(os.getenv("MQTT_PORT", 1883))

        self.client = mqtt.Client()

        # Optional: connection status callback
        self.client.on_connect = self.on_connect

        # Optional: automatic reconnect
        self.client.reconnect_delay_set(min_delay=1, max_delay=10)

        try:
            self.client.connect(self.host, self.port)
            print(f"[MQTT] Connected to {self.host}:{self.port}")
        except Exception as e:
            print(f"[MQTT] ❌ Failed to connect: {e}")

        self.client.loop_start()

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("[MQTT] ✅ Connected successfully.")
        else:
            print(f"[MQTT] ❌ Connect failed with result code {rc}")

    def publish(self, topic, payload):
        result = self.client.publish(topic, payload, qos=1)
        result.wait_for_publish()
        if result.rc == mqtt.MQTT_ERR_SUCCESS:
            print(f"[MQTT] ✅ Published to '{topic}': {payload}")
        else:
            print(f"[MQTT] ❌ Failed to publish to '{topic}' (code: {result.rc})")

# Shared publisher instance
publisher = MQTTPublisher()
=======
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
>>>>>>> master
