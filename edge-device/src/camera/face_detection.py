# camera/face_detection.py
import face_recognition

def detect_face_from_image(image_path):
    try:
        image = face_recognition.load_image_file(image_path)
        face_locations = face_recognition.face_locations(image)
        if face_locations:
            print(f"[FaceDetection] Face(s) found in {image_path}")
            return True
        else:
            print(f"[FaceDetection] No face found in {image_path}")
            return False
    except Exception as e:
        print(f"[FaceDetection] Error processing {image_path}: {e}")
        return False
