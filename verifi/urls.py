from django.urls import path 
from .views import *
from django.http import StreamingHttpResponse

urlpatterns = [

    path('stream/' , VideoView , name='VideoView'),
    path('video_feed/', video_feed, name='video_feed'),
    path('createModel/',model , name='model' ),
    path('faceRecognition/',face_Recognition , name='faceRecognition' ),
    path('information/',information , name='information' ),

]
