import cv2
import math
import threading
import dlib
from .recognition import faceRecognition

class VideoCamera(object):
    def __init__(self):
        self.video1 = cv2.VideoCapture('rtsp://admin:Dd123456@172.16.157.9')
        self.video2 = cv2.VideoCapture('rtsp://admin:Dd123456@172.16.157.10')
        
        if not self.video1.isOpened() or not self.video2.isOpened():
            raise RuntimeError("Could not open one or both cameras")
            
        self.frame_count = 0
        self.lock = threading.Lock()
        self.face_detector = dlib.get_frontal_face_detector()
        
        self.crop_y = (100, 700)
        self.crop_x = 500

    def __del__(self):
        self.video1.release()
        self.video2.release()

    def _crop_frame(self, frame):
        h, w = frame.shape[:2]
        aspect_ratio = w / h
        crop_width = math.floor(self.crop_y[1] - self.crop_y[0]) * aspect_ratio
        return frame[self.crop_y[0]:self.crop_y[1], 
                   self.crop_x:self.crop_x + int(crop_width)]

    def _async_face_recognition(self, frame, cam_id):
        with self.lock:
            filename = f"frame_{self.frame_count}_cam{cam_id}.jpg"
            faceRecognition(filename, frame)

    def get_frame(self):
        # Read frames
        ret1, frame1 = self.video1.read()
        ret2, frame2 = self.video2.read()
        
        if not ret1 or not ret2:
            return b''

        frame1 = self._crop_frame(frame1)
        frame2 = self._crop_frame(frame2)

        combined_frame = cv2.hconcat([frame1, frame2])

        self.frame_count += 1
        if self.frame_count % 10 == 0:
            print(f"Processing frame {self.frame_count}")
            
            t1 = threading.Thread(target=self._async_face_recognition, 
                                args=(frame1.copy(), 1))
            t2 = threading.Thread(target=self._async_face_recognition,
                                args=(frame2.copy(), 2))
            t1.start()
            t2.start()

        _, jpeg = cv2.imencode('.jpg', combined_frame, 
                              [int(cv2.IMWRITE_JPEG_QUALITY), 75])
        return jpeg.tobytes()