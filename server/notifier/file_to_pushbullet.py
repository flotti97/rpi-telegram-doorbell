# import os
# import time
# import logging
# import requests
# from watchdog.observers import Observer
# from watchdog.events import FileSystemEventHandler
# import json

# # Configuration
# WATCH_PATH = r"C:\Users\77079\Documents\JKU\2025 SS\embedded _sys\rpi-telegram-doorbell-main4\rpi-telegram-doorbell-main\server\images"
# SETTINGS_PATH = os.path.join(os.path.dirname(__file__), "config", "settings.json")
# with open(SETTINGS_PATH, "r") as f:
#     settings = json.load(f)

# PUSHBULLET_TOKEN = settings.get("pushbulletToken", "")
# PUSHBULLET_CHANNEL_TAG = settings.get("pushbulletChannelTag", "")
# DOORBELL_NAME = settings.get("doorbellName", "Doorbell")


# # Logging
# logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
# logger = logging.getLogger(__name__)

# def upload_file_to_pushbullet(file_path):
#     file_name = os.path.basename(file_path)
#     with open(file_path, "rb") as f:
#         upload_req = requests.post(
#             "https://api.pushbullet.com/v2/upload-request",
#             headers={"Access-Token": PUSHBULLET_TOKEN},
#             json={"file_name": file_name, "file_type": "image/jpeg"}
#         )
#         upload_data = upload_req.json()
#         upload_url = upload_data["upload_url"]
#         file_url = upload_data["file_url"]
#         files = {'file': (file_name, f, "image/jpeg")}
#         requests.post(upload_url, files=files)
#     return file_name, file_url

# def push_file_to_channel(file_name, file_url):
#     push_req = requests.post(
#         "https://api.pushbullet.com/v2/pushes",
#         headers={"Access-Token": PUSHBULLET_TOKEN, "Content-Type": "application/json"},
#         json={
#             "type": "file",
#             "file_name": file_name,
#             "file_type": "image/jpeg",
#             "file_url": file_url,
#             "body": "New visitor image",
#             "title": DOORBELL_NAME,
#             "channel_tag": PUSHBULLET_CHANNEL_TAG
#         }
#     )
#     if push_req.status_code == 200:
#         logger.info("Pushbullet file sent to channel.")
#     else:
#         logger.error(f"Failed to send file: {push_req.text}")

# class ImageCreatedHandler(FileSystemEventHandler):
#     def on_created(self, event):
#         if not event.is_directory and event.src_path.endswith(".jpg"):
#             time.sleep(1)  # wait for file to finish writing
#             logger.info(f"New image detected: {event.src_path}")
#             try:
#                 file_name, file_url = upload_file_to_pushbullet(event.src_path)
#                 push_file_to_channel(file_name, file_url)
#             except Exception as e:
#                 logger.error(f"Failed to handle image: {e}")

# if __name__ == "__main__":
#     observer = Observer()
#     observer.schedule(ImageCreatedHandler(), path=WATCH_PATH, recursive=False)
#     observer.start()
#     logger.info(f"Watching for new images in {WATCH_PATH}...")
#     try:
#         while True:
#             time.sleep(1)
#     except KeyboardInterrupt:
#         observer.stop()
#     observer.join()
# import os
# import json
# import time
# import logging
# import requests
# import paho.mqtt.client as mqtt
# from threading import Thread
# from watchdog.observers import Observer
# from watchdog.events import FileSystemEventHandler

# # Load config
# SETTINGS_PATH = os.path.join(os.path.dirname(__file__), "config", "settings.json")
# with open(SETTINGS_PATH, "r") as f:
#     settings = json.load(f)

# PUSHBULLET_TOKEN = settings.get("pushbulletToken", "")
# PUSHBULLET_CHANNEL_TAG = settings.get("pushbulletChannelTag", "")
# DOORBELL_NAME = settings.get("doorbellName", "Doorbell")
# MQTT_BROKER = settings.get("mqttBrokerIp", "localhost")
# MQTT_PORT = int(settings.get("mqttBrokerPort", 1883))
# MQTT_TOPIC = settings.get("mqttTopic", "visitor")
# WATCH_PATH = os.path.abspath("../images")

# # Logging
# logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
# logger = logging.getLogger(__name__)

# # Pushbullet functions
# def upload_file_to_pushbullet(file_path):
#     file_name = os.path.basename(file_path)
#     with open(file_path, "rb") as f:
#         upload_req = requests.post(
#             "https://api.pushbullet.com/v2/upload-request",
#             headers={"Access-Token": PUSHBULLET_TOKEN},
#             json={"file_name": file_name, "file_type": "image/jpeg"}
#         )
#         if upload_req.status_code != 200:
#             logger.error(f"Upload request failed: {upload_req.status_code} - {upload_req.text}")
#             raise Exception("Upload request failed")

#         upload_data = upload_req.json()
#         upload_url = upload_data.get("upload_url")
#         file_url = upload_data.get("file_url")
#         if not upload_url or not file_url:
#             logger.error(f"Missing upload_url or file_url in response: {upload_data}")
#             raise Exception("Pushbullet upload response incomplete")

#         files = {'file': (file_name, f, "image/jpeg")}
#         requests.post(upload_url, files=files)
#     return file_name, file_url

# def push_file_to_channel(file_name, file_url, body):
#     push_req = requests.post(
#         "https://api.pushbullet.com/v2/pushes",
#         headers={"Access-Token": PUSHBULLET_TOKEN, "Content-Type": "application/json"},
#         json={
#             "type": "file",
#             "file_name": file_name,
#             "file_type": "image/jpeg",
#             "file_url": file_url,
#             "body": body,
#             "title": DOORBELL_NAME,
#             "channel_tag": PUSHBULLET_CHANNEL_TAG
#         }
#     )
#     if push_req.status_code == 200:
#         logger.info("Pushbullet image sent.")
#     else:
#         logger.error(f"Failed to send image: {push_req.text}")

# def push_note_to_channel(body):
#     push_req = requests.post(
#         "https://api.pushbullet.com/v2/pushes",
#         headers={"Access-Token": PUSHBULLET_TOKEN, "Content-Type": "application/json"},
#         json={
#             "type": "note",
#             "body": body,
#             "title": DOORBELL_NAME,
#             "channel_tag": PUSHBULLET_CHANNEL_TAG
#         }
#     )
#     if push_req.status_code == 200:
#         logger.info("Pushbullet message sent.")
#     else:
#         logger.error(f"Failed to send note: {push_req.text}")

# # Watchdog file watcher
# class ImageCreatedHandler(FileSystemEventHandler):
#     def on_created(self, event):
#         if not event.is_directory and event.src_path.endswith(".jpg"):
#             time.sleep(1)  # ensure file is fully written
#             logger.info(f"New image detected: {event.src_path}")
#             try:
#                 file_name, file_url = upload_file_to_pushbullet(event.src_path)
#                 push_file_to_channel(file_name, file_url, "New visitor image")
#             except Exception as e:
#                 logger.error(f"Failed to handle image: {e}")

# # MQTT client
# def handle_mqtt_payload(payload):
#     logger.info(f"MQTT message received: {payload}")
#     message = payload.get("message", "Visitor alert")
#     filename = payload.get("filename")
#     image_path = payload.get("image_path")

#     if filename:
#         abs_path = os.path.abspath(os.path.join(WATCH_PATH, filename))
#     elif image_path:
#         abs_path = os.path.join(WATCH_PATH, os.path.basename(image_path))
#     else:
#         abs_path = None

#     if abs_path and os.path.exists(abs_path):
#         try:
#             file_name, file_url = upload_file_to_pushbullet(abs_path)
#             push_file_to_channel(file_name, file_url, message)
#         except Exception as e:
#             logger.error(f"Failed to send MQTT image: {e}")
#     else:
#         # If no image, send note only
#         push_note_to_channel(message)

# def mqtt_loop():
#     def on_connect(client, userdata, flags, rc):
#         logger.info(f"Connected to MQTT broker with result code {rc}")
#         client.subscribe(MQTT_TOPIC)

#     def on_message(client, userdata, msg):
#         try:
#             payload = json.loads(msg.payload.decode())
#             handle_mqtt_payload(payload)
#         except Exception as e:
#             logger.error(f"MQTT message error: {e}")

#     client = mqtt.Client()
#     client.on_connect = on_connect
#     client.on_message = on_message
#     client.connect(MQTT_BROKER, MQTT_PORT, 60)
#     client.loop_forever()

# if __name__ == "__main__":
#     # Start file watcher
#     observer = Observer()
#     observer.schedule(ImageCreatedHandler(), path=WATCH_PATH, recursive=False)
#     observer.start()
#     logger.info(f"Watching for new images in {WATCH_PATH}...")

#     # Start MQTT listener in a thread
#     mqtt_thread = Thread(target=mqtt_loop, daemon=True)
#     mqtt_thread.start()

#     try:
#         while True:
#             time.sleep(1)
#     except KeyboardInterrupt:
#         observer.stop()
#     observer.join()

import os
import time
import logging
import requests
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import json

# Configuration
WATCH_PATH = r"C:\Users\77079\Documents\JKU\2025 SS\embedded _sys\rpi-telegram-doorbell-main4\rpi-telegram-doorbell-main\server\images"
SETTINGS_PATH = os.path.join(os.path.dirname(__file__), "config", "settings.json")
with open(SETTINGS_PATH, "r") as f:
    settings = json.load(f)

PUSHBULLET_TOKEN = settings.get("pushbulletToken", "")
PUSHBULLET_CHANNEL_TAG = settings.get("pushbulletChannelTag", "")
DOORBELL_NAME = settings.get("doorbellName", "Doorbell")


# Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

def upload_file_to_pushbullet(file_path):
    file_name = os.path.basename(file_path)
    with open(file_path, "rb") as f:
        upload_req = requests.post(
            "https://api.pushbullet.com/v2/upload-request",
            headers={"Access-Token": PUSHBULLET_TOKEN},
            json={"file_name": file_name, "file_type": "image/jpeg"}
        )
        upload_data = upload_req.json()
        upload_url = upload_data["upload_url"]
        file_url = upload_data["file_url"]
        files = {'file': (file_name, f, "image/jpeg")}
        requests.post(upload_url, files=files)
    return file_name, file_url

def push_file_to_channel(file_name, file_url):
    push_req = requests.post(
        "https://api.pushbullet.com/v2/pushes",
        headers={"Access-Token": PUSHBULLET_TOKEN, "Content-Type": "application/json"},
        json={
            "type": "file",
            "file_name": file_name,
            "file_type": "image/jpeg",
            "file_url": file_url,
            "body": "New visitor image",
            "title": DOORBELL_NAME,
            "channel_tag": PUSHBULLET_CHANNEL_TAG
        }
    )
    if push_req.status_code == 200:
        logger.info("Pushbullet file sent to channel.")
    else:
        logger.error(f"Failed to send file: {push_req.text}")

class ImageCreatedHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith(".jpg"):
            time.sleep(1)  # wait for file to finish writing
            logger.info(f"New image detected: {event.src_path}")
            try:
                file_name, file_url = upload_file_to_pushbullet(event.src_path)
                push_file_to_channel(file_name, file_url)
            except Exception as e:
                logger.error(f"Failed to handle image: {e}")

if __name__ == "__main__":
    observer = Observer()
    observer.schedule(ImageCreatedHandler(), path=WATCH_PATH, recursive=False)
    observer.start()
    logger.info(f"Watching for new images in {WATCH_PATH}...")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
import os
import json
import time
import logging
import requests
import paho.mqtt.client as mqtt
from threading import Thread
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Load config
SETTINGS_PATH = os.path.join(os.path.dirname(__file__), "config", "settings.json")
with open(SETTINGS_PATH, "r") as f:
    settings = json.load(f)

PUSHBULLET_TOKEN = settings.get("pushbulletToken", "")
PUSHBULLET_CHANNEL_TAG = settings.get("pushbulletChannelTag", "")
DOORBELL_NAME = settings.get("doorbellName", "Doorbell")
MQTT_BROKER = settings.get("mqttBrokerIp", "localhost")
MQTT_PORT = int(settings.get("mqttBrokerPort", 1883))
MQTT_TOPIC = settings.get("mqttTopic", "visitor")

# Set the absolute path for the images directory
WATCH_PATH = "/home/admin/rpi-telegram-doorbell/server/images"  # Make sure to use absolute path

# Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

# Pushbullet functions
def upload_file_to_pushbullet(file_path):
    file_name = os.path.basename(file_path)
    with open(file_path, "rb") as f:
        upload_req = requests.post(
            "https://api.pushbullet.com/v2/upload-request",
            headers={"Access-Token": PUSHBULLET_TOKEN},
            json={"file_name": file_name, "file_type": "image/jpeg"}
        )
        if upload_req.status_code != 200:
            logger.error(f"Upload request failed: {upload_req.status_code} - {upload_req.text}")
            raise Exception("Upload request failed")

        upload_data = upload_req.json()
        upload_url = upload_data.get("upload_url")
        file_url = upload_data.get("file_url")
        if not upload_url or not file_url:
            logger.error(f"Missing upload_url or file_url in response: {upload_data}")
            raise Exception("Pushbullet upload response incomplete")

        files = {'file': (file_name, f, "image/jpeg")}
        requests.post(upload_url, files=files)
    return file_name, file_url

def push_file_to_channel(file_name, file_url, body):
    push_req = requests.post(
        "https://api.pushbullet.com/v2/pushes",
        headers={"Access-Token": PUSHBULLET_TOKEN, "Content-Type": "application/json"},
        json={
            "type": "file",
            "file_name": file_name,
            "file_type": "image/jpeg",
            "file_url": file_url,
            "body": body,
            "title": DOORBELL_NAME,
            "channel_tag": PUSHBULLET_CHANNEL_TAG
        }
    )
    if push_req.status_code == 200:
        logger.info("Pushbullet image sent.")
    else:
        logger.error(f"Failed to send image: {push_req.text}")

def push_note_to_channel(body):
    push_req = requests.post(
        "https://api.pushbullet.com/v2/pushes",
        headers={"Access-Token": PUSHBULLET_TOKEN, "Content-Type": "application/json"},
        json={
            "type": "note",
            "body": body,
            "title": DOORBELL_NAME,
            "channel_tag": PUSHBULLET_CHANNEL_TAG
        }
    )
    if push_req.status_code == 200:
        logger.info("Pushbullet message sent.")
    else:
        logger.error(f"Failed to send note: {push_req.text}")

# Watchdog file watcher
class ImageCreatedHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory and event.src_path.endswith(".jpg"):
            time.sleep(1)  # ensure file is fully written
            logger.info(f"New image detected: {event.src_path}")
            try:
                file_name, file_url = upload_file_to_pushbullet(event.src_path)
                push_file_to_channel(file_name, file_url, "New visitor image")
            except Exception as e:
                logger.error(f"Failed to handle image: {e}")

# MQTT client
def handle_mqtt_payload(payload):
    logger.info(f"MQTT message received: {payload}")
    message = payload.get("message", "Visitor alert")
    filename = payload.get("filename")
    image_path = payload.get("image_path")

    if filename:
        abs_path = os.path.abspath(os.path.join(WATCH_PATH, filename))
    elif image_path:
        abs_path = os.path.join(WATCH_PATH, os.path.basename(image_path))
    else:
        abs_path = None

    if abs_path and os.path.exists(abs_path):
        try:
            file_name, file_url = upload_file_to_pushbullet(abs_path)
            push_file_to_channel(file_name, file_url, message)
        except Exception as e:
            logger.error(f"Failed to send MQTT image: {e}")
    else:
        push_note_to_channel(message)

def mqtt_loop():
    def on_connect(client, userdata, flags, rc):
        logger.info(f"Connected to MQTT broker with result code {rc}")
        client.subscribe(MQTT_TOPIC)

    def on_message(client, userdata, msg):
        logger.info(f"Received message: {msg.payload.decode()}")
        try:
            payload = json.loads(msg.payload.decode())
            handle_mqtt_payload(payload)
        except Exception as e:
            logger.error(f"MQTT message error: {e}")

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(MQTT_BROKER, MQTT_PORT, 60)
    client.loop_forever()

if __name__ == "__main__":
    # Start file watcher
    observer = Observer()
    observer.schedule(ImageCreatedHandler(), path=WATCH_PATH, recursive=False)
    observer.start()
    logger.info(f"Watching for new images in {WATCH_PATH}...")

    # Start MQTT listener in a thread
    mqtt_thread = Thread(target=mqtt_loop, daemon=True)
    mqtt_thread.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
