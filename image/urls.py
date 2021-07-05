from django.urls import path
from .views import *

urlpatterns = [
    path('', upload, name = 'upload'),
    path('frame', frame, name = 'frame'),
    path('video', video, name = 'video'),
    path('stream', stream, name = 'stream'),
    path('save_config', save_config, name = 'save_config')
]