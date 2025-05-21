import subprocess
import os

class SoundPlayer:
    def __init__(self, sound_file_name):
        base_dir = os.path.dirname(__file__)
        self.sound_file = os.path.join(base_dir, sound_file_name)
        self.device = "plughw:2,0"  # Audio output device

    def play(self):
        if not os.path.exists(self.sound_file):
            print(f"[Error] Sound file not found: {self.sound_file}")
            return
        subprocess.run(["aplay", "-D", self.device, self.sound_file], check=True)

# Shared instance for reuse
player = SoundPlayer("doorbell.wav")
