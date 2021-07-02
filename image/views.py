
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
            object = action.cleaned_data.get('imageField')
            config = action.cleaned_data.get('imageConfig')
            image, path = create(object)
            test_process(image, config)
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


def pre_process(data, path):
    image = open(path, "wb")
    image.write(data)
    test_process(path, 0.4)
    image.close()


def frame(request):
    if request.method == 'POST':
        data = b64decode(request.POST.get('data'))
        name = random.choices(string.ascii_lowercase, k = 7)
        name = ''.join(name) + '.jpg'
        path = Path.joinpath(media_root, 'video', name)
        pre_process(data, path)
        result = {'path': '/media/video/' + name}
    return HttpResponse(json.dumps(result), content_type='application/json')
