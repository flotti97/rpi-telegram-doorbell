import time
import os
import subprocess

IMAGE_SAVE_DIR = "/mnt/samba"

def capture_snapshot(prefix="snap"):
    if os.path.exists(IMAGE_SAVE_DIR) and not os.path.isdir(IMAGE_SAVE_DIR):
        raise RuntimeError(f"{IMAGE_SAVE_DIR} exists but is not a directory. Check Samba mount.")

    os.makedirs(IMAGE_SAVE_DIR, exist_ok=True)

    timestamp = int(time.time())
    filename_tmp = f"{prefix}_{timestamp}.tmp"
    filename_final = f"{prefix}_{timestamp}.jpg"

    filepath_tmp = os.path.join(IMAGE_SAVE_DIR, filename_tmp)
    filepath_final = os.path.join(IMAGE_SAVE_DIR, filename_final)

    try:
        subprocess.run([
            "libcamera-still", "-n", "-o", filepath_tmp,
            "--width", "640", "--height", "480"
        ], check=True)

        os.rename(filepath_tmp, filepath_final)

        print(f"[Snapshot] Captured: {filepath_final}")
        return filepath_final
    except subprocess.CalledProcessError as e:
        print(f"[Error] Failed to capture snapshot: {e}")
        return None
    except Exception as e:
        print(f"[Error] Failed to rename snapshot: {e}")
        return None
