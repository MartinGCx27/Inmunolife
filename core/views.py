import pdb
from django.core.validators import validate_integer
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from django.urls import reverse_lazy, reverse
from django.contrib import messages 
from django.conf import settings
from .models import Contactos, Register  #no se estaban importando el modelo Register, se agrega -LGS
from .forms import FormContact, RegisterForm, LoginForm, PasswordResetRequestForm, PasswordResetForm
from django.contrib.auth.hashers import make_password, check_password
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
import hashlib
import time
import secrets
from datetime import timedelta
from django.utils import timezone



class inmunolife_home(CreateView):
    model = Contactos
    form_class = FormContact
    template_name = 'index.html'
    success_url = reverse_lazy('home')
    prefix = 'contact'

    def get_context_data(self, **kwargs):  #se agrega el get_context_data para maquetar ambos formularios -LGS
        context = super().get_context_data(**kwargs)
        context['register_form'] = RegisterForm(prefix="register")
        context['login_form'] = LoginForm(prefix="login")
        return context

    def form_valid(self, form):
        # Mensaje éxito contacto (tags: 'success contact')
        messages.success(self.request, '¡Mensaje de contacto enviado con éxito!', extra_tags="contact") #Se agrega el extra_tags para el FormContact para envio exitoso -LGS
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Error en el formulario de contacto', extra_tags="contact") #Se agrega el extra_tags para el FormContact para envio exitoso-LGS
        return super().form_invalid(form)  #Renderiza el template con el formulario inválido -LGS

# Función para registrar usuarios -Emix
def register_user(request):
    if request.method == "POST":  # Verifica si la solicitud es de tipo POST -Emix
        register_form = RegisterForm(request.POST, prefix="register")  # Crea una instancia del formulario de registro con los datos enviados y le asigna un prefijo "register" -LGS
        contact_form = FormContact(prefix="contact")  # Crea una instancia del formulario de contacto con el prefijo "contact" -Emix

        if register_form.is_valid():  # Verifica si el formulario es válido -Emix
            user = register_form.save(commit=False)  # Guarda el usuario pero aún no lo almacena en la base de datos -Emix
            user.passrd = make_password(register_form.cleaned_data['passrd'])  # Encripta la contraseña antes de guardarla -Emix
            user.save()  # Guarda el usuario en la base de datos -Emix
            # Mensaje éxito registro (tags: 'success register') -Emix
            messages.success(request, "¡Registro exitoso, favor de iniciar sesión!", extra_tags="register")  # Envía un mensaje de éxito con la etiqueta "register" -Emix
            return redirect("home")  # Redireccionamos a home para no tener problemas con los formularios -Emix
        else:
            # Mensaje error registro (tags: 'error register') -Emix
            messages.error(request, "Error en el registro, correo y/o celular ya registrados", extra_tags="register")  # Envía un mensaje de error con la etiqueta "register" -Emix
            # Redireccionamos a home con un parámetro en la URL que indique que se deben mostrar los errores en el modal de registro -Emix
            return redirect(reverse("home") + "?modal=register")
    
    # Si la solicitud no es POST, renderiza index.html con todos los formularios vacíos -Emix
    return render(request, "index.html", {
        "form": FormContact(prefix="contact"),  # Instancia vacía del formulario de contacto -Emix
        "register_form": RegisterForm(prefix="register"),  # Instancia vacía del formulario de registro -Emix
        "login_form": LoginForm(prefix="login")  # Instancia vacía del formulario de inicio de sesión -Emix
    })

    
#Función para el captcha -Emix
def index_page(request):
  # Comprueba si la solicitud actual es de tipo POST -Emix
  if request.method == 'POST':
    # Obtiene el token de respuesta del reCAPTCHA -Emix
    recaptcha_response = request.POST.get('g-recaptcha-response')
    # Prepara los datos necesarios para verificar el reCAPTCHA -Emix
    data = {
      'secret': settings.RECAPTCHA_SECRET_KEY, # Clave secreta del reCAPTCHA configurada en settings.py-Emix
      'response': recaptcha_response # Token de respuesta del reCAPTCHA enviado por el usuario-Emix
    }
    # Establece la URL de verificación del reCAPTCHA de Google-Emix
    verify_url = 'https://www.google.com/recaptcha/api/siteverify'
    # Realiza una solicitud POST a la URL de verificación -Emix
    response = request.post(verify_url, data=data)
    # Convierte la respuesta de la solicitud a un formato JSON para procesar los resultados-Emix
    result = response.json()
    # Comprueba si la verificación del reCAPTCHA fue exitosa-Emix
    if result.get('success'):
      # Si la verificación es exitosa, redirige al usuario a una página de éxito-Emix
      return redirect('success')
    else:
      # Si la verificación falla, muestra un mensaje de error al usuario-Emix
      messages.error(request, 'Verificación del reCAPTCHA fallida. Por favor, inténtelo de nuevo')    
  # Si la solicitud no es POST, simplemente renderiza la página de inicio-Emix
  return render(request, 'index.html')


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST) #Instancia del formulario de login -LGS
        if form.is_valid():
            email = form.cleaned_data['loginEmail']
            password = form.cleaned_data['loginPassword']
            
            try:
                user = Register.objects.get(email=email) #ayudara a validar si en register existe email -LGS
                if check_password(password, user.passrd):  
                    messages.success(request, "¡Bienvenidoooo!", extra_tags="login") # si existe el email dara una bienvenida -LGS
                    return redirect('home')
                else:
                    messages.error(request, "Contraseña incorrecta", extra_tags="login")
            except Register.DoesNotExist:
                messages.error(request, "El correo no está registrado", extra_tags="login")
        else:
            for error in form.errors.values():
                messages.error(request, error[0], extra_tags="login")
        
        return render(request, "index.html")
    return redirect('home')

#Función para generar el token personalizado -LGS
def generate_reset_token(user):
    #Genera un token único y aleatorio para el restablecimiento de contraseña -LGS
    token = secrets.token_urlsafe()  # Genera un token seguro -LGS
    print(f"Generated token: {token}")
    user.reset_token = token  # Asigna el token al usuario -LGS
    user.reset_token_expiration = timezone.now() + timedelta(hours=1)  #indicamos que el token expira en 1 hora -LGS
    user.save()
    return token

#Valida si el token es válido y no ha expirado.
def validate_reset_token(user, token):
    if user.reset_token != token:
        return False
    if user.reset_token_expiration and user.reset_token_expiration < timezone.now():
        return False  #El token ha expirado
    return True

# Vista principal para manejar solicitudes de restablecimiento de contraseña -LGS
def password_reset_request(request):
    if request.method == "POST":  #Procesamos datos del formulario enviado -LG
        email = request.POST.get("email")
        user = Register.objects.filter(email=email).first()

        if user:
            #Genera el token personalizado y guárda en la base de datos -LG
            token = generate_reset_token(user)
            user.reset_token = token #Almacena token en el usuario -LG
            user.save()

            #Genera la URL para el enlace de restablecimiento de contraseña -LGS
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            reset_url = request.build_absolute_uri(
                reverse('password_reset_confirm', kwargs={'uidb64': uidb64, 'token': token})
            )

            print(f"Reset URL: {reset_url}")  #Verifica la URL generada -LGS

            #Envío de email con enlace de restablecimiento -LGS
            send_mail(
                "Restablecimiento de Contraseña",
                f"Para restablecer tu contraseña, haz clic en el siguiente enlace:\n\n{reset_url}",
                "noreply@tuapp.com",
                [user.email],
                fail_silently=False,
            )

            
            return redirect("password_reset_done")  #Redirige a la página de éxito -LGS
        else:
            messages.error(request, "No existe una cuenta con este correo.", extra_tags="password_reset")

    form = PasswordResetRequestForm() 
    return render(request, "password_reset_request.html", {"form": form})


#Vista para manejar la confirmación del restablecimiento de contraseña.
def password_reset_confirm(request, uidb64, token):    
    try:
        # Decodifica el ID del usuario desde la URL
        uid = urlsafe_base64_decode(uidb64).decode()
        # Obtiene el usuario de la base de datos usando el ID -LGS
        user = Register.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Register.DoesNotExist):
        user = None #verifica si el usuario existe

    if user and validate_reset_token(user, token):
        if request.method == "POST":
            form = PasswordResetForm(request.POST)
            if form.is_valid():
                new_password = form.cleaned_data['new_password']
                #Actualiza la contraseña con hash seguro -LGS
                user.password = make_password(new_password)
                user.reset_token = None #Ayuda a invalidar token usado -LGS
                user.reset_token_expiration = None #Ayuda a invalidar token expirado -LGS
                user.save()  #Guarda los cambios en la base de datos -LGS

                messages.success(request, "Tu contraseña ha sido cambiada con éxito.", extra_tags="password_reset")
                return redirect("password_reset_complete")
            else:
                messages.error(request, "Las contraseñas no coinciden, favor de corregir.", extra_tags="password_reset")
        else:
            form = PasswordResetForm()
        
        # Pasar el nombre de usuario al contexto
        context = {
            "form": form,
            "username": user.name  #darle el nombre y contexto para llamar al usuario en el template -LGS
        }
        return render(request, "password_reset_confirm.html", context)
    else:
        messages.error(request, "El enlace no es válido o ha expirado.", extra_tags="password_reset")
        return redirect("password_reset")

#funcion simple para renderizar el templete que dice "correo enviado" -LGS
def password_reset_done(request):
    return render(request, "password_reset_done.html")

#funcion simple para renderizar el templete que dice "cambio completado de contraseña"
def password_reset_complete(request):
    return render(request, "password_reset_complete.html")


#Función para el Login -Emix
#@login_required
# def login(request):
#     last_user = Register.objects.order_by('-id').first()  #para pruebgas de starter page muestre el nombre de usuario -LGS
#      #print("Último usuario registrado:", last_user)
#     return render(request, 'starter-page.html', {'last_user': last_user})

# def login_view(request):
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             # Validación de la cuenta y contraseña
#             email = form.cleaned_data.get('email')
#             password = form.cleaned_data.get('password')

#             try:
#                 user = Register.objects.get(email=email)
#                 if user.passrd == password:
#                     messages.success(request, 'Inicio de sesión exitoso.')
#                     return redirect('starter-page')  # Cambia la URL de redirección según tu proyecto
#                 else:
#                     messages.error(request, 'Contraseña incorrecta.')
#             except Register.DoesNotExist:
#                 messages.error(request, 'No existe una cuenta con este correo.')
#         else:
#             messages.error(request, 'Revisa los errores e intenta nuevamente.')
#     else:
#         form = LoginForm()

#     return render(request, 'index.html', {'form_login': form})