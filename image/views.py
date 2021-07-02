
from django.shortcuts import render
from django.conf import settings
from django.http import StreamingHttpResponse
from pathlib import Path
from .forms import Upload
from .models import Image
from .utils import test_process
from .utils import true_process
import cv2

def upload(request):
    path = ''
    if request.method == 'POST':
        action = Upload(request.POST, request.FILES)
        if action.is_valid():
            object = action.cleaned_data.get('imageField')
            config = action.cleaned_data.get('imageConfig')
            image, path = create(object)
            true_process(image, config)
        else:
            print('No Image Uploaded')
    return render(request, 'index.html', {'path': path})


def create(object):
    data = Image.objects.create(image = object)
    path = data.image.url
    name = Path(path).name
    root = settings.MEDIA_ROOT
    image = Path.joinpath(root, 'images', name)
    return image, path


def video(request):
    return render(request, 'video.html')


def stream(request):
    return StreamingHttpResponse(extract(), content_type='multipart/x-mixed-replace; boundary=frame')


def extract():
    cap = cv2.VideoCapture(0) 

    while True:
        ret, frame = cap.read()
        path = 'media/videos/demo.jpg'

        if not ret:
            print("Error: failed to capture image")
            break

        cv2.imwrite(path, frame)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + open(path, 'rb').read() + b'\r\n')