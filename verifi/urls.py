from django.urls import path 
from .views import *
from django.http import StreamingHttpResponse

app_name = 'verifi'

urlpatterns = [

    path('stream/' , VideoView , name='VideoView'),
    path('video_feed/', video_feed, name='video_feed'),
    path('cameraView/', cameraView, name='cameraView'),

    path('createModel/',model , name='createModel' ),
    path('camera_view/<str:personnelNumber>',camera_view , name='camera_view' ),
    path('save_photo/',save_photo , name='save_photo' ),
    path('uploadImage/<str:personnelNumber>' , uploadImage , name='uploadImage'),


    # path('savePoint/',savePoint , name='savePoint' ),
    path('faceRecognition/',face_Recognition , name='faceRecognition' ),
    # path('information/',information , name='information' ),
    path('log/' , logView , name='log'),
    path('result/',result,name='result')

]
