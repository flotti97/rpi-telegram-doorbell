import RPi.GPIO as GPIO
import time
from event.handler import handle_button_event

BUTTON_PIN = 16  # GPIO pin for the button

def run_button_loop():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    try:
        print("Waiting for button press...")
        while True:
            if GPIO.input(BUTTON_PIN) == GPIO.LOW:
                print("Button pressed!")
                handle_button_event()
                time.sleep(0.3)
            time.sleep(0.1)
    except KeyboardInterrupt:
        GPIO.cleanup()
        print("\nExiting...")
