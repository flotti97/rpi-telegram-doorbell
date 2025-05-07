import RPi.GPIO as GPIO
import subprocess
import time

# Set up button on Gpio 16
BUTTON_PIN = 16

#path to wav
MUSIC_FILE = "/home/admin/Downloads/rpi-telegram-doorbell-main/edge-device/src/sound/doorbell.wav"

#initialize GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

print("Waiting for button press...")

try:
        while True:
                if GPIO.input(BUTTON_PIN) == GPIO.LOW:
                        print("Button pressed! Play doorbell sound...")
                        subprocess.run(["aplay", MUSIC_FILE], check=True)
                        time.sleep(0.3)
                time.sleep(0.1)
except KeyboardInterrupt:
        GPIO.cleanup()
        print("\nExitting...")
