import cv2
from django.http import HttpResponse
import time
import dlib
from .models import *
import math
from .recognition import faceRecognition

error_face = []
countdown = 6
face_cascade = cv2.CascadeClassifier("./haarcascade_frontalface_default.xml")
detector = dlib.get_frontal_face_detector()


def saveCrop(name, imge):
    if imge is not None:
        faces = face_cascade.detectMultiScale(
            imge, scaleFactor=1.1, minNeighbors=5, minSize=(40, 40)
        )
        multipale = []

        for item in faces:
            if len(item) == 0:
                cv2.imwrite(f"./media/false/{name}", faces)

            else:
                multipale.append(item)

            p = 0
            if faces is not tuple:
                for x, y, w, h in multipale:
                    face_roi = imge[y:y + h, x:x + w]
                    p += 1
                    saveFace(f"{p}_{name}", face_roi)


def saveFace(name, image):
    try:
        face = detector(image)
        if face:

            Face.objects.create(name=f"{name}", noise=True)
            faceRecognition(name, image)


        else:
            print('false1')
    except:
        print('false11')


class VideoCamera(object):
    def __init__(self):
        # Using OpenCV to capture from device 0. If you have trouble capturing
        # from a webcam, comment the line below out and use a video file
        # instead.
        self.video = cv2.VideoCapture('rtsp://admin:Dd123456@172.16.157.9')  #.rtsp://admin:Dd123456@172.16.157.9 & rtsp://admin:Dd123456@172.16.157.10'
        self.frame_count = 0
        self.frame_count1 = 0
        # If you decide to use video.mp4, you must have this file in the folder
        # as the main.py.

    def __del__(self):
        self.video.release()


    def get_frame(self):
        success, frame = self.video.read()
        if not success:
            return HttpResponse('not success')
        # We are using Motion JPEG, but OpenCV defaults to capture raw images,
        # so we must encode it into JPEG in order to correctly display the
        # video stream.

        # w, h = frame.shape[:2]
        # w_new = 2000
        #
        # retion = w / h
        #
        # h_new = int(w_new * retion)
        #
        # frame = cv2.resize(frame, (w_new, h_new), interpolation=cv2.INTER_LINEAR)


        w, h = frame.shape[:2]

        n_retion = h / w
        frame = frame[100:700, 500:500+math.floor((700-100)*n_retion)]
        # print(frame.shape[:2])

        self.frame_count1 += 1
        # resize and shape [2] frame  video stream
        # print(time.time() % 2)
        # if time.time() % 2 < 0.1:
        if self.frame_count1 % 10 == 0 :
            self.frame_count += 1
            print(self.frame_count)

            saveFace(f"frame_{self.frame_count}.jpg", frame)

        # w, h = frame.shape[:2]
        # new_w = int(w * 2.0)
        # new_h = int(h * 2.0)
        #
        # frame = cv2.resize(frame, (new_w, new_h), interpolation=cv2.INTER_AREA)
        # #
        # sX, sY = 300, 300
        # eX, eY = 800, 800
        #
        # frame = frame[sY:eY, sX:eX]
        ret, jpeg = cv2.imencode('.jpg', frame)

        return jpeg.tobytes()
