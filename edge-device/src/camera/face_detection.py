# File: edge-device/src/camera/face_detection.py

import cv2
import os

# Load Haar Cascade classifier from local models folder
BASE_DIR = os.path.dirname(__file__)
CASCADE_PATH = os.path.join(BASE_DIR, "haarcascade_frontalface_default.xml")

# Initialize the CascadeClassifier
face_cascade = cv2.CascadeClassifier(CASCADE_PATH)

def detect_face_from_image(image_path):
    """
    Detects faces in the specified image using OpenCV Haar Cascade.
    Returns True if at least one face is found, False otherwise.
    """
    # Read the input image
    image = cv2.imread(image_path)
    if image is None:
        print(f"[FaceDetection] Unable to read image file: {image_path}")
        return False

    # Convert the image to grayscale for face detection
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Perform face detection
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )

    if len(faces) > 0:
        print(f"[FaceDetection] Detected {len(faces)} face(s) in {image_path}")
        return True
    else:
        print(f"[FaceDetection] No faces found in {image_path}")
        return False
