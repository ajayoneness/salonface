from . import views
from django.urls import path

urlpatterns = [
    path('cam/',views.opencv,name="camera" ),
    path('face/',views.video, name ="video")
]
