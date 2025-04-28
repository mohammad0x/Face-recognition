import cv2
import numpy as np
import dlib
from .models import *

face_cascade = cv2.CascadeClassifier("./haarcascade_frontalface_default.xml")
predictor = dlib.shape_predictor("./shape_predictor_68_face_landmarks.dat")
face_recognizer = dlib.face_recognition_model_v1(
    "./dlib_face_recognition_resnet_model_v1.dat"
)
detector = dlib.get_frontal_face_detector()


def Crop(name, imge):
    if imge is not None:
        faces = face_cascade.detectMultiScale(
            imge, scaleFactor=1.1, minNeighbors=5, minSize=(20, 20)
        )

        multipale = []

        for item in faces:
            if len(item) == 0:
                pass

            else:
                multipale.append(item)

            p = 0
            if faces is not tuple:
                for x, y, w, h in multipale:
                    face_roi = imge[y:y + h, x:x + w]
                    p += 1
                    extract_face_descriptor(name, np.array(face_roi) )

def extract_face_descriptor(name , image ):
    try:
        faces = detector(image)
    except:
        pass
    if len(faces) == 1:

        landmarks = predictor(image, faces[0])

        face_descriptor = face_recognizer.compute_face_descriptor(image, landmarks)
        Dbmodel.objects.filter(name=name).update(point=np.array(face_descriptor) )
        return name , np.array(face_descriptor)
    else:
        return False