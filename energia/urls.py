from django.urls import path
from . import views

urlpatterns = [
    path('energia', views.upload_file, name='upload_file'),
    path('energia/edistribucion', views.edistribucion, name='edistribucion'),
]