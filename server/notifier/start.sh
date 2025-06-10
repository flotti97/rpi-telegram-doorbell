#!/bin/bash
source activate doorbell-notifier
exec uvicorn mqtt_to_pushbullet:app --host 0.0.0.0 --port 8000
