# button.py
import RPi.GPIO as GPIO
import time
import json
from sound_service import player  # Sound logic
from mqtt_publisher import publisher  # MQTT logic

BUTTON_PIN = 16

# GPIO Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def handle_button_press():
    """Combined action handler"""
    print("Button pressed!")
    player.play()  # Sound logic separated
    
    publisher.publish(
        topic="visitor",
        payload=json.dumps({
            "event": "button_pressed",
            "timestamp": time.time(),
            "location": "front_door"
        })
    )

# Main loop remains exactly the same
try:
    print("Waiting for button press...")
    while True:
        if GPIO.input(BUTTON_PIN) == GPIO.LOW:
            handle_button_press()
            time.sleep(0.3)
        time.sleep(0.1)
except KeyboardInterrupt:
    GPIO.cleanup()
    print("\nExiting...")
