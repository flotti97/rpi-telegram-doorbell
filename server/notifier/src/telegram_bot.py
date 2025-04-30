import os
import paho.mqtt.client as mqtt
from telegram import Bot

# Set your Telegram bot token and chat ID (use env vars or config in production)
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "YOUR_TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "YOUR_CHAT_ID")

MQTT_BROKER = os.getenv("MQTT_BROKER", "localhost")
MQTT_PORT = int(os.getenv("MQTT_PORT", 1883))
MQTT_TOPIC = "visitor"

bot = Bot(token=TELEGRAM_TOKEN)

def send_telegram_message(text):
    bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=text)

def on_connect(client, userdata, flags, rc):
    print("Connected to MQTT broker with result code " + str(rc))
    client.subscribe(MQTT_TOPIC)

def on_message(client, userdata, msg):
    print(f"MQTT message received: {msg.topic} {msg.payload}")
    if msg.topic == MQTT_TOPIC:
        send_telegram_message("Visitor detected at the door!")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_forever()