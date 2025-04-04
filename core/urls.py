from django.urls import path
# from django.contrib.auth.views import LoginView, logout_then_login
from . import views
#Se importa vista creada en views -LGS
from .views import inmunolife_home
from django.contrib import admin
from django.conf.urls import handler500


handler500 = views.error_500_view 

# URLS from App Core

urlpatterns = [
    #URL ADMIN -LGS
    # path('admin/', admin.site.urls),
    # Home
    #Ruta para la vista llamando la clase crerada en views -LGS
    path('', inmunolife_home.as_view(), name='home'),
    #Ruta para la view de login -Emix
    path('login/', views.login_view, name='login'),
    # Registrar usuario -Emix
    path('register/', views.register_user, name='register_user'),
    #URL para confirmar existencia de correo -LGS
    path('password_reset/', views.password_reset_request, name='password_reset'),
    #URL para modificar la contraseña -LGS
    path('password_reset_confirm/<str:uidb64>/<str:token>/', views.password_reset_confirm, name='password_reset_confirm'),
    #URL para vista de confirmacion de envio de correo -LGS
    path('password_reset_done/', views.password_reset_done, name='password_reset_done'),
    #URL de cambio hecho exitosamente -LGS
    path('password_reset_complete/', views.password_reset_complete, name='password_reset_complete'),
    #Ruta para el login exitoso -Emix
    path('inicio/', views.login_successful, name='login_successful'),
    #Ruta para el logout 
    path('logout/', views.logout_view, name='logout'),
    #Ruta para error 404
    path('error404/', views.error404_view, name='error 404'),
    path('force_error/', views.error_500_view, name='force_error')
    # path("error500/", views.trigger_error)
]

