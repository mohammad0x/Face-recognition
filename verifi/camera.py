import cv2
from django.http import HttpResponse
import dlib
from .recognition import faceRecognition
import math
import threading

error_face = []
countdown = 6
face_cascade = cv2.CascadeClassifier("./haarcascade_frontalface_default.xml")
detector = dlib.get_frontal_face_detector()


class VideoCamera(object):
    def __init__(self):
        # Using OpenCV to capture from device 0. If you have trouble capturing
        # from a webcam, comment the line below out and use a video file
        # instead.

        # if 2 camera
        self.video = cv2.VideoCapture(1)  #.rtsp://admin:Dd123456@172.16.157.9 & rtsp://admin:Dd123456@172.16.157.10'
        # self.video2 =cv2.VideoCapture(1)

        # if 2 camera
        # if not self.video2.isOpened():
        #     print("Error: Could not open camera 1.")
        #     exit()

        if not self.video.isOpened():
            print("Error: Could not open camera 2.")
            exit()

        self.frame_count = 0
        self.frame_count1 = 0

        # self.lock = threading.Lock()

        # If you decide to use video.mp4, you must have this file in the folder
        # as the main.py.

    def __del__(self):

        self.video.release()
        # self.video2.release()
        # self.input_images.release()

    def get_frame(self):

        # if 2 camera
        success, frame = self.video.read()
        # success, frame2 = self.video2.read()
        if not success:
            return HttpResponse('not success')

        # if 2 camera
        # self.input_images = cv2.hconcat([frame1 , frame2 ])

        # We are using Motion JPEG, but OpenCV defaults to capture raw images,
        # so we must encode it into JPEG in order to correctly display the
        # video stream.

        # if zoom and crop 

        # w, h = frame.shape[:2]
        #
        # n_retion = h / w
        # frame = frame[100:700, 500:500+math.floor((700-100)*n_retion)]

        # if 2 camera

        # frame = []
        # frame.append(frame1)
        # frame.append(frame2)

        self.frame_count1 += 1
        if self.frame_count1 % 10 == 0:
            self.frame_count += 1
            print(self.frame_count)

            # if 2 camera
            # for i , f in enumerate(frame):
            faceRecognition(f"frame_{self.frame_count}.jpg", frame)

        ret, jpeg = cv2.imencode('.jpg',frame)

        return jpeg.tobytes()

    # def get_frame(self):
    #     def process_frame(video, camera_id):
    #         nonlocal frame1, frame2
    #         success, frame = video.read()
    #         if not success:
    #             return

    #         with self.lock:
    #             if camera_id == 1:
    #                 frame1 = frame
    #             else:
    #                 frame2 = frame

    #             self.frame_count1 += 1
    #             if self.frame_count1 % 10 == 0:
    #                 self.frame_count += 1
    #                 print(self.frame_count)
    #                 faceRecognition(f"frame_{self.frame_count}.jpg", frame)

    #     frame1, frame2 = None, None

    #     thread1 = threading.Thread(target=process_frame, args=(self.video1, 1))
    #     thread2 = threading.Thread(target=process_frame, args=(self.video2, 2))

    #     thread1.start()
    #     thread2.start()

    #     thread1.join()
    #     thread2.join()

    #     if frame1 is not None and frame2 is not None:
    #         self.input_images = cv2.hconcat([frame1, frame2])
    #         ret, jpeg = cv2.imencode('.jpg', self.input_images)
    #         return jpeg.tobytes()
    #     else:
    #         return HttpResponse('not success')
