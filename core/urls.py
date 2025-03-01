from django.urls import path
# from django.contrib.auth.views import LoginView, logout_then_login
from . import views
#Se importa vista creada en views -LGS
from .views import inmunolife_home


 

# URLS from App Core

urlpatterns = [
    # Home
    #Ruta para la vista llamando la clase crerada en views -LGS
    path('', inmunolife_home.as_view(), name='home'),
    #Login
    path('login/', views.login, name="login"),
    # Registrar usuario
    path('', views.register_user, name="register_user")
    
]
