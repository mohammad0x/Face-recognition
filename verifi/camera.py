import cv2
from django.http import HttpResponse
import dlib
from .recognition import faceRecognition

error_face = []
countdown = 6
face_cascade = cv2.CascadeClassifier("./haarcascade_frontalface_default.xml")
detector = dlib.get_frontal_face_detector()


class VideoCamera(object):
    def __init__(self):
        # Using OpenCV to capture from device 0. If you have trouble capturing
        # from a webcam, comment the line below out and use a video file
        # instead.
        self.video = cv2.VideoCapture(0)  #.rtsp://admin:Dd123456@172.16.157.9 & rtsp://admin:Dd123456@172.16.157.10'
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
        #
        # n_retion = h / w
        # frame = frame[100:700, 500:500+math.floor((700-100)*n_retion)]

        self.frame_count1 += 1
        if self.frame_count1 % 10 == 0:
            self.frame_count += 1
            print(self.frame_count)

            faceRecognition(f"frame_{self.frame_count}.jpg", frame)
      
        ret, jpeg = cv2.imencode('.jpg', frame)

        return jpeg.tobytes()
