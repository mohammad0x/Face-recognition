import cv2
from django.http import HttpResponse
import time
import dlib
import os
import numpy as np
from .models import *
from .recognition import faceRecognition

error_face = []

face_cascade = cv2.CascadeClassifier("../haarcascade_frontalface_default.xml")
detector = dlib.get_frontal_face_detector()

def saveCrop(name,imge):
    # loop = []

    # for item , imge in enumerate(os.listdir("./media/test/")):
    # loop.append(name)
    # print(loop)
    # unique_list = list(set(loop))

    # print(unique_list)
    # for item , image in enumerate(unique_list):
        # image = f"./media/test/{img}"
        # image = cv2.imread(img)

    # print(imge)
    if imge is not None:
        faces = face_cascade.detectMultiScale(
            imge, scaleFactor=1.1, minNeighbors=5, minSize=(20, 20)
        )
        # cv2.imwrite(f"./media/crop/_{name}", faces)
        # print(faces)
        multipale = []
            
        for item in faces:
            if len(item) == 0:
                cv2.imwrite(f"./media/false/{name}", faces)

            else:
                multipale.append(item)

            p = 0
            if faces is not tuple:
                for x, y, w, h in multipale:
                    face_roi = imge[y:y+h, x:x+w]
                    p += 1
                    saveFace(f"{p}_{name}", face_roi)



def saveFace(name , image):

    try:
        face = detector(image)
        if face:
            try:

                Face.objects.create(name=f"{name}",noise=True)
                faceRecognition(name,image)
                # cv2.imwrite(f"./media/crop/{name}", image)

            except:
                pass
        else:
                # if cv2.imwrite(f"./media/noise/{img}", image):
            # os.remove(f"./media/crop/{name}")
            pass
    except:
        pass
        # continue
        # Face.objects.filter(name=imagee).update(noise=True)


class VideoCamera(object):
    def __init__(self):
        # Using OpenCV to capture from device 0. If you have trouble capturing
        # from a webcam, comment the line below out and use a video file
        # instead.
        self.video = cv2.VideoCapture(1)#./rest2.mp4
        # self.extracted_frames = []
        self.frame_count = 0
        # If you decide to use video.mp4, you must have this file in the folder
        # as the main.py.
        # self.video = cv2.VideoCapture('video.mp4')
    
    def __del__(self):
        self.video.release()
    
    def get_frame(self):
        output_path = './media/test/'
        success, frame = self.video.read()
        if not success:
            return HttpResponse('not success')
        # We are using Motion JPEG, but OpenCV defaults to capture raw images,
        # so we must encode it into JPEG in order to correctly display the
        # video stream.
        if time.time() % 2 < 0.1:
            # self.extracted_frames.append(frame)

            self.frame_count += 1
            print(self.frame_count)
            # cv2.imwrite(f"{output_path}frame_{self.frame_count}.jpg", frame)
            # j = cv2.imread('./2.jpg')
            saveCrop(f"frame_{self.frame_count}.jpg", frame)
            # if self.frame_count > 2:
                # os.remove(f"{output_path}frame_{self.frame_count-1}.jpg")
            # saveCrop()
            
        ret, jpeg = cv2.imencode('.jpg', frame)
        
        return jpeg.tobytes()


