from django.shortcuts import render
from .camera import VideoCamera
from .laboratory import savePoint
from .recognition import faceRecognition
from .models import *
import time
from django.http.response import StreamingHttpResponse
from django.views.decorators.cache import never_cache

# Create your views here.

def model(request):
    if request.method == 'POST':
        image = request.FILES['image']
        name = request.POST['name']
        Dbmodel.objects.create(name=name, image=image)
    return render(request , 'model.html')

@never_cache
def VideoView(request):
    countdown = 1
    # faceRecognition.apply_async(countdown=countdown)   #apply_async()
    return render(request , 'stream.html' )

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def video_feed(request):
    return StreamingHttpResponse(gen(VideoCamera()),
                    content_type='multipart/x-mixed-replace; boundary=frame')
def face_Recognition(request):
    time.sleep(6)
    faceRecognition()
    return render(request , 'facerecognition.html')

def information(request):
    res_t = Result.objects.filter(noise=False).order_by('-date')[:9]
    res_f = Face.objects.filter(noise=True).order_by('-date')[:9]
    trueResult= []
    falseResult = []
    for result in res_t:
        trueResult.append({'image' : f"http://127.0.0.1:8000/{result.recognition.split('/')[1]}/old/{result.recognition.split('/')[3]}"
                     , 'name': result.name , 'date': result.date})
    for result in res_f:
        falseResult.append({'image' : f"http://127.0.0.1:8000/{result.name.split('/')[1]}/unknow/{result.name.split('/')[3]}"
                     , 'name': result.name , 'date': result.date})

    context = {
        'trueResults': trueResult,
        'falseResult': falseResult,
    }
    return render(request , 'information.html' , context)