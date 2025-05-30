import dlib
import cv2
import numpy as np
import shutil
from .models import *
import logging
from .views import *
from django.utils.timezone import now, make_aware
from django.shortcuts import render, redirect
from datetime import datetime, timedelta
from jdatetime import datetime as jdatetime_datetime
import requests
from django.contrib import messages



logger = logging.getLogger(__name__)

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





    


def extract_face_descriptor(name, image):
    try:
        faces = detector(image)
    except:
        pass

    if len(faces) > 0:

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        landmarks = predictor(gray, faces[0])

        face_descriptor = face_recognizer.compute_face_descriptor(image, landmarks)
        return np.array(face_descriptor)
    else:
        return False


def faceRecognition(name, image):
    while True:
        threshold = 0.6

        db_face = []

        point = extract_face_descriptor(name, np.array(image))

        if point is False:
            break

        clean = []
        name_clean = []
        face = Dbmodel.objects.all()
        for face in face:
            clean.append(face.point)
            name_clean.append(face.name)

        for num in range(len(clean)):
            fix = clean[num].replace("[", "").replace("]", "")
            value = fix.split()
            aray = [item for item in value]
            dbmodel_2 = []
            for item in aray:
                try:
                    dbmodel_2.append(float(item))
                except:
                    pass
            db_face.append(np.array(dbmodel_2))

        for item in range(len(db_face)):
            distance = np.linalg.norm(db_face[item] - point)
            if distance < threshold:
                if Result.objects.filter(recognition=name).exists():
                    break

                last_entry = Result.objects.filter(name=name_clean[item],
                                                   date=jdatetime_datetime.now().strftime('%d %B %Y')).order_by(
                    '-time').first()
                if last_entry:

                    last_entry_datetime = datetime.combine(now().date(), last_entry.time)
                    last_entry_datetime = make_aware(last_entry_datetime)
                    current_datetime = now()

                    time_diff = current_datetime - last_entry_datetime
                    if time_diff.total_seconds() < 10:
                        log.objects.create(name=name_clean[item],status = 'duplicate')
                        cv2.imwrite(f"./media/old/photo.jpg", image)
                        return 'duplicate'
                  

                if Result.objects.create(name=name_clean[item], recognition=name):
                    log.objects.create(name=name_clean[item],status = 'create')
                    cv2.imwrite(f"./media/old/photo.jpg", image)
                    return 'create'




            else:
                pass

        # unknown

        if not Result.objects.filter(recognition=name).exists():
            cv2.imwrite(f"./media/unknow/unknown.jpg", image)
            log.objects.create(name=name,status = 'unknown')   
            return 'unknown'


        break


            
       
        

# celery -A FaceGuard worker -l info
