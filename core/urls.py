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
    path('/login', views.login_view, name='login'),
    # Registrar usuario
    path('/register', views.register_user, name='register_user'),
    #URL para confirmar existencia de correo -LGS
    path('password_reset/', views.password_reset_request, name='password_reset'),
    #URL para modificar la contraseña -LGS
    path('password_reset_confirm/<str:uidb64>/<str:token>/', views.password_reset_confirm, name='password_reset_confirm'),
    #URL para vista de confirmacion de envio de correo -LGS
    path('password_reset_done/', views.password_reset_done, name='password_reset_done'),
    #URL de cambio hecho exitosamente -LGS
    path('password_reset_complete/', views.password_reset_complete, name='password_reset_complete'),
    path('login/', views.login_view, name='login'),
    path('inicio/', views.starter_page, name='starter_page'),
    path('logout/', views.logout_view, name='logout'),
]