from django.urls import path
from . import views

# URLS from App Core

urlpatterns = [
    # Home
    path('', views.inmunolife_home, name='home')
]
