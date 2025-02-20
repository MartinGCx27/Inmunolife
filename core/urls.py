from django.contrib import admin
from django.urls import path
# from django.contrib.auth.views import LoginView, logout_then_login
from . import views

#Se importa vista creada en views -LGS
from .views import inmunolife_home


 

# URLS from App Core

urlpatterns = [
<<<<<<< HEAD
<<<<<<< HEAD
    # Home
    #Ruta para la vista llamando la clase crerada en views -LGS
    path('', inmunolife_home.as_view(), name='home'),
=======
=======
>>>>>>> e61f65b0ee301ef82194474740e42b75e1e35462
    path('', inmunolife_home.as_view(), name='home'),
    
    # Home
    #Ruta para la vista llamando la clase crerada en views -LGS
    
<<<<<<< HEAD
>>>>>>> e61f65b0ee301ef82194474740e42b75e1e35462
=======
>>>>>>> e61f65b0ee301ef82194474740e42b75e1e35462
    # path('', views.inmunolife_home, name='home'),
    #Login de admin(?) -Emix
    #path('', LoginView.as_view,{'template_name':'index.html'}, name = 'login'),
    #Logout de admin (?) -Emix
    #path('logout/', logout_then_login, name='logout'),
    
    # Registrar usuario
    path("register/", views.register_user, name="register_user")
    
]

