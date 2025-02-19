from django.urls import path
# from . import views

#Se importa vista creada en views -LGS
from .views import inmunolife_home

# URLS from App Core

urlpatterns = [
    # Home
    # path('', views.inmunolife_home, name='home')
    #Ruta para la vista llamando la clase crerada en views -LGS
    path('', inmunolife_home.as_view(), name='home'),
]
