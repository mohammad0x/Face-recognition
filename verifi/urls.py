from django.urls import path 
from .views import *
from django.http import StreamingHttpResponse

app_name = 'verifi'

urlpatterns = [

    path('stream/' , VideoView , name='VideoView'),
    path('video_feed/', video_feed, name='video_feed'),
    path('createModel/',model , name='model' ),
    path('savePoint/',savePoint , name='savePoint' ),
    path('faceRecognition/',face_Recognition , name='faceRecognition' ),
    path('information/',information , name='information' ),

]
