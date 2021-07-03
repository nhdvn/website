
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


def mkfile():
    name = random.choices(string.ascii_lowercase, k = 7)
    name = ''.join(name) + '.jpg'
    path = Path.joinpath(media_root, 'video')
    Path(path).mkdir(parents = True, exist_ok = True)
    return name, Path.joinpath(path, name)


def write(data):
    name, path = mkfile()
    image = open(path, "wb")
    image.write(data)
    image.close()
    return name, path


def frame(request):
    if request.method == 'POST':
        config = request.POST.get('config')
        model = request.POST.get('model')
        data = b64decode(request.POST.get('data'))
        name, path = write(data)

        true_process(path, float(config), model)
        result = {'path': '/media/video/' + name}
        return HttpResponse(json.dumps(result), content_type = 'application/json')
    else:
        return HttpResponse()
