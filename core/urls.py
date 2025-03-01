from django.urls import path
# from django.contrib.auth.views import LoginView, logout_then_login
from . import views
#Se importa vista creada en views -LGS
from .views import inmunolife_home
from django.contrib.auth import views as auth_views


 

# URLS from App Core

urlpatterns = [
    # Home
    #Ruta para la vista llamando la clase crerada en views -LGS
    path('', inmunolife_home.as_view(), name='home'),
    #Login
    path('login/', views.login, name="login"),
    # Registrar usuario
    path('registro', views.register_user, name='register_user'),

    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='registration/password_reset_form.html',  # Tu plantilla
        email_template_name='registration/password_reset_email.html',  # Plantilla de correo personalizada
        subject_template_name='registration/password_reset_subject.txt',  # Asunto del correo
        success_url='/password_reset/done/'
    ), name='password_reset'),

    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='registration/password_reset_done.html'
    ), name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='registration/password_reset_confirm.html',
        
        success_url='/reset/done/'
    ), name='password_reset_confirm'),

    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='registration/password_reset_complete.html'
    ), name='password_reset_complete'),
]
