import dlib
import cv2
import numpy as np
import shutil
from .models import *
from celery import shared_task
import os
import logging
from  .views import *
import time

logger = logging.getLogger(__name__)

error_face = []
false_face = []
noyz_face = []

known_face_encodings = []
known_face_names = []

predictor = dlib.shape_predictor("../shape_predictor_68_face_landmarks.dat")
face_recognizer = dlib.face_recognition_model_v1(
    "../dlib_face_recognition_resnet_model_v1.dat"
)
detector = dlib.get_frontal_face_detector()


def extract_face_descriptor(image):
    try:
        faces = detector(image)
    except:
        pass #faceRecognition()#.delay()
    if len(faces) == 1:

        landmarks = predictor(image, faces[0])

        face_descriptor = face_recognizer.compute_face_descriptor(image, landmarks)
        return np.array(face_descriptor)
    else:
        return False

# @shared_task
def faceRecognition(name , image):
    while True:
        threshold = 0.4


        new_face = []
        name_face = []
        db_face = []
        reference_image_new = []
        base_dir = './media/' #Path(__file__).resolve().parent.parent
        # time.sleep(2)



        # for img in os.listdir("./media/crop"):
        #     time.sleep(1)
        #     img = f"./media/crop/{img}"
        # image = cv2.imread(img)
        #
        # if Face.objects.filter(name=name, verify=True):
        #         try:
        #             os.remove(f"./media/crop/{name}")
        #         except:
        #             pass
        point = extract_face_descriptor(np.array(image))
        if Face.objects.filter(name=name , noise=True):
            Face.objects.filter(name=name).update(point=point)

            name_face.append(name)
        # reference_image = image
        # print(name)
        try:
            Face.objects.filter(name=name).update(point=point)
        except:
            pass


        facee = Face.objects.filter(verify=False)
        for faces in facee:
            reference_image_new.append(faces.point)

        # for num in range(len(reference_image_new)):
        #     if reference_image_new[num] is not None :
        #         fix = reference_image_new[num].replace("[", "").replace("]", "")
        #         value = fix.split()
        #         aray = [item for item in value]
        #         dbmodel = []
        #         for item in aray:
        #             try:
        #                 dbmodel.append(float(item))
        #             except:
        #                 pass
        #         new_face.append(np.array(dbmodel))
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
        # time.sleep(2)

        for item in range(len(db_face)):
            # for number in range(len(new_face)):
            #     if len(new_face[number]) != 0:
            distance = np.linalg.norm(db_face[item] - point)# new_face[number]
            if distance < threshold:
                # try:
                    if Result.objects.filter(recognition=name).exists():
                        video_feed()
                    if Result.objects.create(name=name_clean[item], recognition=name):#name_face[number]
                            Face.objects.filter(name=name).update(verify=True)
                            # cv2.imwrite(f"./media/old/{name}", image)
                                #shutil.move(f'{name_face[number]}',
                                       # f'./{name_face[number].split("/")[1]}/old/')

            else:
                video_feed()

                        #         if f'./old/{name_face[number].split("/")[3]}':
                        #             # print(f'./media/crop/{name_face[number].split("/")[3]}')
                        #             Face.objects.filter(name=f'./media/crop/{name_face[number].split("/")[3]}').update(verify=True)
                        #
                # except:
                #     print('not')
                #     break


        #     else:
        #
        #                 try:
        #                     time.sleep(1.5)
        #                     shutil.move(f'{name_face[number]}',
        #                                 f'./{name_face[number].split("/")[1]}/unknow/')
        #                 except:
        #                     pass
        # continue

# celery -A FaceGuard worker -l info
print('finish')