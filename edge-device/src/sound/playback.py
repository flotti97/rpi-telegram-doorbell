# sound_service.py
import subprocess

class SoundPlayer:
    def __init__(self, sound_file):
        self.sound_file = sound_file
    
    def play(self):
        subprocess.run(["aplay", self.sound_file], check=True)

# Initialize with your sound file
player = SoundPlayer("/home/admin/Downloads/rpi-telegram-doorbell-main/edge-device/src/sound/doorbell.wav")
