from django.shortcuts import render, redirect
from .camera import VideoCamera
from .laboratory import savePoint
from .recognition import faceRecognition
from .models import *
from django.urls import reverse
import time
import numpy as np
from PIL import Image
import cv2
from django.views.decorators.csrf import csrf_exempt
import base64
import os
from django.conf import settings
from django.http import JsonResponse
from django.http.response import StreamingHttpResponse, HttpResponse
from .recognition import extract_face_descriptor
from .attendance import attendance
from .picture import PictureCamera


@csrf_exempt
def save_photo(request):
    if request.method == 'POST':
        photo_data = request.POST.get('photo')
        personnelNumber = request.POST['personnelNumber']

        if photo_data and personnelNumber:

            format, imgstr = photo_data.split(';base64,')
            ext = format.split('/')[-1]
            img_data = base64.b64decode(imgstr)

            photo_path = os.path.join(settings.MEDIA_ROOT, 'photos', 'photo.jpg')
            os.makedirs(os.path.dirname(photo_path), exist_ok=True)
            with open(photo_path, 'wb') as f:
                f.write(img_data)

            image = cv2.imread('./media/photos/photo.jpg')
            result = extract_face_descriptor(personnelNumber, np.array(image))
            outcome = Dbmodel.objects.filter(personnelNumber=personnelNumber).update(point=result)

            if outcome == 1:
                if Dbmodel.objects.filter(personnelNumber=personnelNumber, point=False):
                    return JsonResponse({'status': 'False'})

                return JsonResponse({'status': 'success',
                                     'path': photo_path,
                                     'redirect_url': reverse('verifi:createModel'),
                                     })

    return JsonResponse({'status': 'error'}, status=400)


def model(request):
    if request.method == 'POST':
        name = request.POST['name']
        personnelNumber = request.POST['personnelNumber']
        date_of_birth = request.POST['date_of_birth']
        field = request.POST['field']

        Dbmodel.objects.create(name=name,
                               personnelNumber=personnelNumber,
                               date_of_birth=date_of_birth,
                               field=field)

        return render(request, 'response.html', {'personnelNumber': personnelNumber})
    return render(request, 'model.html')


def uploadImage(request, personnelNumber):
    if request.method == 'POST' and request.FILES['image']:
        image = request.FILES['image']
        img = Image.open(image)

        result = extract_face_descriptor(personnelNumber, np.array(img))

        Dbmodel.objects.filter(personnelNumber=personnelNumber).update(point=result)

        return HttpResponse('saved picture')
    return render(request, 'image.html')


def VideoView(request):
    # countdown = 6
    # faceRecognition()#.apply_async(countdown=countdown)   #apply_async()

    return render(request, 'stream.html')


def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


def video_feed(request):
    return StreamingHttpResponse(gen(VideoCamera()),
                                 content_type='multipart/x-mixed-replace; boundary=frame')


def cameraView(request):
    return StreamingHttpResponse(gen(PictureCamera()),
                                 content_type='multipart/x-mixed-replace; boundary=frame')


def camera_view(request, personnelNumber):
    return render(request, 'camera.html', {'personnelNumber': personnelNumber})


def face_Recognition(request):
    time.sleep(6)
    faceRecognition()
    return render(request, 'facerecognition.html')


def logView(request):
    context = {
        'log': log.objects.all().order_by('-time')
    }
    return render(request, 'log.html', context)


def result(request):
    return render(request, 'result.html')
# def information(request):
#     res_t = Result.objects.filter(noise=False).order_by('-date')
#     res_f = Face.objects.filter(verify=False).order_by('-date')
#     trueResult = []
#     falseResult = []
#     for result in res_t:
#         print(result.recognition)
#         trueResult.append({'image': f"http://127.0.0.1:8000/media/old/{result.recognition}"
#                               , 'name': result.name, 'date': result.date})
#     for result in res_f:
#         falseResult.append({'image': f"http://127.0.0.1:8000/media/unknow/{result.name}"
#                                , 'name': result.name, 'date': result.date})
#
#     context = {
#         'trueResults': trueResult,
#         'falseResult': falseResult,
#     }
#     return render(request, 'information.html', context)
