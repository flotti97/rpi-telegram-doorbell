import time
import threading
import paho.mqtt.client as mqtt
import json

BROKER = "localhost"
PORT = 1883
TOPIC = "visitor"

def on_connect(client, userdata, flags, rc, properties=None):
    if (rc != 0):
        print("Connection failed with code " + str(rc))
        return
    else:
        print("Connected to MQTT broker successfully")
    client.subscribe(TOPIC)

def on_message(client, userdata, msg, properties=None):
    print(f"Received message: {msg.payload.decode()} on topic {msg.topic}")

def run_subscriber():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(BROKER, PORT, 60)
    client.loop_forever()

def run_publisher():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.connect(BROKER, PORT, 60)
    
    payload = {
        "message": "Visitor",
        "filename": "Starry_Night.jpg"
    }
    message = json.dumps(payload)
    client.publish(TOPIC, message, qos=1)
    print(f"Published: {message}")
    
    client.disconnect()

if __name__ == "__main__":
    # sub_thread = threading.Thread(target=run_subscriber, daemon=True)
    # sub_thread.start()
    # time.sleep(2)

    pub_thread = threading.Thread(target=run_publisher)
    pub_thread.start()
    pub_thread.join()
    time.sleep(2)