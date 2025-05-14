import os
import json
import paho.mqtt.client as mqtt
import requests

# Load settings from settings.json
SETTINGS_PATH = os.path.join(os.path.dirname(__file__), "settings.json")
with open(SETTINGS_PATH, "r") as f:
    settings = json.load(f)

MQTT_BROKER = settings.get("mqttBrokerIp", "localhost")
MQTT_PORT = int(settings.get("mqttBrokerPort", 1883))
MQTT_TOPIC = settings.get("mqttTopic", "visitor")

PUSHBULLET_TOKEN = "o.sQgQk595YDtwO8larza1tgqB8tFBaHK2"  # Set your Pushbullet Access Token as an environment variable
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
        print("Pushbullet file sent to channel.")
    else:
        print(f"Failed to send file: {push_req.text}")

def send_pushbullet_file_to_channel(token, channel_tag, file_path, title, body):
    file_name, file_url = upload_file_to_pushbullet(token, file_path)
    push_file_to_channel(token, channel_tag, file_name, file_url, title, body)

def handle_mqtt_payload(payload):
    message = payload.get("message", "Visitor")
    filename = payload.get("filename")
    if filename:
        image_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "fileshare", "samba", filename))
        if os.path.exists(image_path):
            send_pushbullet_file_to_channel(
                PUSHBULLET_TOKEN,
                PUSHBULLET_CHANNEL_TAG,
                image_path,
                "Doorbell Event",
                message
            )
        else:
            print(f"Image not found: {image_path}")
    else:
        print("No filename provided in payload.")

def on_connect(client, userdata, flags, rc, properties=None):
    print("Connected to MQTT broker with result code " + str(rc))
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg, properties=None):
    try:
        payload = json.loads(msg.payload.decode())
        handle_mqtt_payload(payload)
    except Exception as e:
        print(f"Error handling MQTT message: {e}")

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_forever()