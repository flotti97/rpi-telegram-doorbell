import time
import os
import subprocess

# Absolute path to save snapshots
IMAGE_SAVE_DIR = "/mnt/samba"

def capture_snapshot(prefix="snap"):
    os.makedirs(IMAGE_SAVE_DIR, exist_ok=True)
    timestamp = int(time.time())
    filename = f"{prefix}_{timestamp}.jpg"
    filepath = os.path.join(IMAGE_SAVE_DIR, filename)

    try:
        subprocess.run([
            "libcamera-still", "-n", "-o", filepath,
            "--width", "640", "--height", "480"
        ], check=True)
        print(f"[Snapshot] Captured: {filepath}")
        return filepath
    except subprocess.CalledProcessError as e:
        print(f"[Error] Failed to capture snapshot: {e}")
        return None
