import cv2
import face_recognition

def recognize(arg, frame):
    face_locations = face_recognition.face_locations(frame)
    for face_location in face_locations:
        (top, right, bottom, left) = face_location
        cv2.rectangle(frame, (left, top), (right, bottom), (170, 255, 127), 2)
    return frame

