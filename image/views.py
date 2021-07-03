
from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse
from base64 import b64decode
from pathlib import Path
from .forms import Upload
from .models import Image
from .utils import test_process
from .utils import true_process
import json, random, string

media_root = settings.MEDIA_ROOT


def upload(request):
    path = ''
    if request.method == 'POST':
        action = Upload(request.POST, request.FILES)
        if action.is_valid():
            object = action.cleaned_data.get('object')
            config = action.cleaned_data.get('config')
            model = action.cleaned_data.get('model')
            print(model)
            image, path = create(object)
            true_process(image, config, model)
        else:
            print('No Image Uploaded')
    return render(request, 'index.html', {'path': path})


def create(object):
    data = Image.objects.create(image = object)
    name = Path(data.image.url).name
    image = Path.joinpath(media_root, 'image', name)
    return image, data.image.url


def video(request):
    return render(request, 'video.html')


def mkdir(file_name):
    path = Path.joinpath(media_root, 'video')
    Path(path).mkdir(parents = True, exist_ok = True)
    path = Path.joinpath(path, file_name)
    return path


def write(data, file):
    path = mkdir(file)
    image = open(path, "wb")
    image.write(data)
    test_process(path, 0.4)
    image.close()


def frame(request):
    if request.method == 'POST':
        data = b64decode(request.POST.get('data'))
        file = ''.join(random.choices(string.ascii_lowercase, k = 7)) + '.jpg'
        write(data, file)
        result = {'path': '/media/video/' + file}
        return HttpResponse(json.dumps(result), content_type = 'application/json')
    else:
        return HttpResponse()
