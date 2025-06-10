import time
import os
import json
from snapshot.capture import capture_snapshot
from camera.face_detection import detect_face_from_image
from sound.playback import player
from mqtt.publisher import publisher

TRIGGER_INTERVAL = 5  # seconds
_last_trigger_time = 0

def handle_button_event():
    global _last_trigger_time
    now = time.time()

    if now - _last_trigger_time < TRIGGER_INTERVAL:
        print("[Info] Ignored button press (within interval)")
        return
    _last_trigger_time = now

    print("[Event] Button pressed → capturing and playing sound...")

    # Step 1: Take snapshot and get file path
    filepath = capture_snapshot("face")
    if not filepath:
        print("[Error] Snapshot failed.")
        return

    # Step 2: Play doorbell sound
    player.play()

    # Step 3: Face detection
    if not detect_face_from_image(filepath):
        print("[Info] No face detected. No MQTT published.")
        return

    print("[Detect] Face detected → sending MQTT...")

    # Step 4: Publish MQTT message
    filename = os.path.basename(filepath)
    print("[MQTT] Will publish:")
    print(json.dumps({
    "message": "Visitor detected",
    "filename": filename
}))
    publisher.publish(
        topic="visitor",
        payload=json.dumps({
            "message": "Visitor detected",
            "filename": filename
    })
)
