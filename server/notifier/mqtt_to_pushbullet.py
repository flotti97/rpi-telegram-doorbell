import os
import json
import paho.mqtt.client as mqtt
import requests
from fastapi import FastAPI
from threading import Thread
import logging

logging.basicConfig(
    level=os.environ.get("LOG_LEVEL", "INFO").upper(),
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI()

class MQTTManager:
    def __init__(self):
        self.client = None
        self.connected = False
        self.thread = None
        self.load_settings()

    def load_settings(self):
        SETTINGS_PATH = os.path.join(os.path.dirname(__file__), "config", "settings.json")
        with open(SETTINGS_PATH, "r") as f:
            content = f.read()
            self.settings = json.loads(content)
        self.MQTT_BROKER = self.settings.get("mqttBrokerIp", "localhost")
        self.MQTT_PORT = int(self.settings.get("mqttBrokerPort", 1883))
        self.MQTT_TOPIC = self.settings.get("mqttTopic", "visitor")

    def on_connect(self, client, userdata, flags, rc, properties=None):
        logger.info(f"Connected to MQTT broker with result code {rc}")
        client.subscribe(self.MQTT_TOPIC)
        self.connected = True

    def on_message(self, client, userdata, msg, properties=None):
        try:
            payload = json.loads(msg.payload.decode())
            handle_mqtt_payload(payload)
        except Exception as e:
            logger.error(f"Error handling MQTT message: {e}")

    def connect(self):
        if self.connected:
            return "Already connected"
        self.load_settings()
        self.client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(self.MQTT_BROKER, self.MQTT_PORT, 60)
        self.thread = Thread(target=self.client.loop_forever, daemon=True)
        self.thread.start()
        return "Connecting..."

    def disconnect(self):
        if self.client and self.connected:
            self.client.disconnect()
            self.connected = False
            return "Disconnected"
        return "Not connected"

mqtt_manager = MQTTManager()
mqtt_manager.connect()

# --- Pushbullet functions

PUSHBULLET_TOKEN = "o.sQgQk595YDtwO8larza1tgqB8tFBaHK2"
PUSHBULLET_CHANNEL_TAG = "eps_doorbell"

def upload_file_to_pushbullet(token, file_path):
    file_name = os.path.basename(file_path)
    with open(file_path, "rb") as f:
        upload_req = requests.post(
            "https://api.pushbullet.com/v2/upload-request",
            headers={"Access-Token": token},
            json={"file_name": file_name, "file_type": "image/jpeg"}
        )
        upload_data = upload_req.json()
        upload_url = upload_data["upload_url"]
        file_url = upload_data["file_url"]
        files = {'file': (file_name, f, "image/jpeg")}
        requests.post(upload_url, files=files)
    return file_name, file_url

def push_file_to_channel(token, channel_tag, file_name, file_url, title, body):
    push_req = requests.post(
        "https://api.pushbullet.com/v2/pushes",
        headers={"Access-Token": token, "Content-Type": "application/json"},
        json={
            "type": "file",
            "file_name": file_name,
            "file_type": "image/jpeg",
            "file_url": file_url,
            "body": body,
            "title": title,
            "channel_tag": channel_tag
        }
    )
    if push_req.status_code == 200:
        logger.info("Pushbullet file sent to channel.")
    else:
        logger.error(f"Failed to send file: {push_req.text}")

def send_pushbullet_file_to_channel(token, channel_tag, file_path, title, body):
    file_name, file_url = upload_file_to_pushbullet(token, file_path)
    push_file_to_channel(token, channel_tag, file_name, file_url, title, body)

def handle_mqtt_payload(payload):
    message = payload.get("message", "Visitor")
    filename = payload.get("filename")
    if filename:
        image_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "app", "images", filename))
        if os.path.exists(image_path):
            send_pushbullet_file_to_channel(
                PUSHBULLET_TOKEN,
                PUSHBULLET_CHANNEL_TAG,
                image_path,
                "Doorbell Event",
                message
            )
        else:
            logger.error(f"Image not found: {image_path}")
    else:
        logger.error("No filename provided in payload.")

# --- FastAPI endpoints ---

@app.post("/mqtt/connect")
def api_connect():
    return {"status": mqtt_manager.connect()}

@app.post("/mqtt/disconnect")
def api_disconnect():
    return {"status": mqtt_manager.disconnect()}