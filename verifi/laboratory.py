import dlib
import cv2
import numpy as np
from .models import *
import os



error_face = []
false_face = []
noyz_face = []


known_face_encodings = []
known_face_names = []



predictor = dlib.shape_predictor("./shape_predictor_68_face_landmarks.dat")
face_recognizer = dlib.face_recognition_model_v1(
    "./dlib_face_recognition_resnet_model_v1.dat"
)
detector = dlib.get_frontal_face_detector()


def extract_face_descriptor(image):
    faces = detector(image)

    if len(faces) == 1:
        landmarks = predictor(image, faces[0])

        face_descriptor = face_recognizer.compute_face_descriptor(image, landmarks)
        return np.array(face_descriptor)
    else:
        return False


def savePoint(name):
    image = f"./media/faces/{name}.jpg"
    reference_image = cv2.imread(image)

    if extract_face_descriptor(reference_image) is not False:
            Dbmodel.objects.filter(name=name).update(point=extract_face_descriptor(reference_image))
            known_face_names.append(name)
