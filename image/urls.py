from django.urls import path
from .views import upload, video, stream

urlpatterns = [
    path('', upload, name = 'upload'),
    path('stream', stream, name = 'stream'),
    path('video', video, name = 'video')
]