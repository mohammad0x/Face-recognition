import cv2
from django.http import HttpResponse
import math



class PictureCamera(object):
    def __init__(self):
        # Using OpenCV to capture from device 0. If you have trouble capturing
        # from a webcam, comment the line below out and use a video file
        # instead.


        self.video =cv2.VideoCapture(1)  #.rtsp://admin:Dd123456@172.16.157.9 & rtsp://admin:Dd123456@172.16.157.10'
        if not self.video.isOpened():
            print("Error: Could not open camera 1.")
            exit()


        
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
        
        # n_retion = h / w
        # frame = frame[100:700, 500:500+math.floor((700-100)*n_retion)]


    
        
        ret, jpeg = cv2.imencode('.jpg', frame)

        return jpeg.tobytes()