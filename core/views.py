import pdb
from django.core.validators import validate_integer
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, TemplateView
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
import requests
from django.http import HttpResponseServerError



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
        messages.error(self.request, 'Error en el formulario de contacto. Por favor vuelve a intentarlo', extra_tags="contact") #Se agrega el extra_tags para el FormContact para envio exitoso-LGS
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
            messages.error(request, "Error en el registro, correo y/o celular ya registrados. Por favor vuelve a intentarlo", extra_tags="register")  # Envía un mensaje de error con la etiqueta "register" -Emix
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

#Función para login -LGS
def login_view(request):
    # Vista principal para el proceso de inicio de sesión
    if request.method == 'POST':
        # Verificación de datos recibidos -LGS
        print("Datos recibidos:", request.POST)  # Debug que muestra los datos del formulario -LGS
        
        # Validación de reCAPTCHA -LGS
        recaptcha_response = request.POST.get('g-recaptcha-response')  # Obtiene la respuesta del captcha
        secret_key = settings.RECAPTCHA_SECRET_KEY  # Clave secreta desde settings.py
        data = {'secret': secret_key, 'response': recaptcha_response}
        
        # Verificación con servidor de Google para que funcione el captcha -LGS
        response = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
        captcha_result = response.json()
        print("Respuesta reCAPTCHA:", captcha_result)  # Depuración: Muestra respuesta de Google
        
        # Manejo de fallos en reCAPTCHA -LGS
        if not captcha_result.get('success'):
            messages.error(request, 'Error en el reCAPTCHA. Por favor intentelo de nuevo', extra_tags="login")
            return redirect('home')

        # Proceso de autenticación manual -LGS
        email = request.POST.get('loginEmail')  # Obtiene el correo ingresado
        password = request.POST.get('loginPassword')  # Obtiene la contraseña ingresada
        
        try:
            # Búsqueda de usuario por email -LGS
            user = Register.objects.get(email=email)
            print("Usuario encontrado:", user)  # Depuración: Confirma usuario encontrado -LGS
            print(f"Contraseña ingresada: '{password}'")  # Debug de contraseña ingresada -Emix
            print(f"Hash almacenado: '{user.passrd}'")  # Debug de contraseña hasheada -Emix
            print(f"¿Coinciden?: {check_password(password, user.passrd)}")  # Verifica coincidencia

            #Validación de usuario activo -LGS
            if not user.user_active:
                messages.error(request, 'No se pudo iniciar sesión, usuario inactivo. Contacta a soporte.', extra_tags="login")
                return redirect(reverse("home") + "?modal=login")

            # Verificación de contraseña existente -LGS
            if check_password(password, user.passrd):
                print("Contraseña válida")  # Depuración: Confirma contraseña correcta -LGS
                
                # Creación de sesión de usuario -LGS
                request.session['user_id'] = user.id  # Almacena ID de usuario -LGS
                request.session['logged_in'] = True  # Bandera de autenticación -LGS
                request.session.set_expiry(3600)  # Expiración de sesión en 1 hora (3600 segundos) -LGS
                
                # print("Sesión después de login:", request.session.items())  # Debug que muestra datos de sesión -LGS
                
                return redirect('login_successful')  # Redirección a página protegida -LGS
            else:
                # Mensaje de contraseña incorrecta -LGS
                print("Contraseña incorrecta")
                messages.error(request, 'Contraseña incorrecta. Por favor intentelo de nuevo', extra_tags="login")
        
        except Register.DoesNotExist:
            # Mensaje de usuario no registrado -LGS
            print("Usuario no existe")
            messages.error(request, 'Usuario no registrado. Por favor intentelo de nuevo', extra_tags="login")
        
        # Redirección con parámetro para mostrar modal de login y no perder la vista -LGS
        return redirect(reverse("home") + "?modal=login")
    
    # Redirección si el método no es POST -LGS
    return redirect('home')

def login_required_custom(view_func):
    # Decorador personalizado para protección de rutas
    def wrapper(request, *args, **kwargs):
        #Verificación de estado de sesión -LGS
        print("Verificando sesión:", request.session.get('logged_in'))  # Depuración
        
        #Validación de autenticación -LGS
        if not request.session.get('logged_in'):
            messages.error(request, 'Debes iniciar sesión para acceder')
            return redirect('home')  # Redirección si no está autenticado

        #Ejecución de la vista protegida si está autenticado -LGS
        return view_func(request, *args, **kwargs)
    return wrapper


#Vista principal protegida que muestra información del usuario -LGS
@login_required_custom
def login_successful(request):

    try:
        # Obtener datos del usuario actual desde la sesión -LGS
        user_id = request.session.get('user_id')
        print(f"ID de usuario en sesión: {user_id}")  #Depuración id del usuario -LGS
        
        #Obtener objeto del usuario actual 
        current_user = Register.objects.get(id=user_id)
        
        #Obtener último usuario registrado -LGS
        last_registered_user = Register.objects.order_by('-id').first()
        
        #Debug de datos
        print(f"Usuario actual: {current_user.email}")
        print(f"Último registrado: {last_registered_user.email if last_registered_user else 'Ninguno'}")
        

        context = {
            'user': current_user, #Usuario autenticado en la base de datosd -LGS
            'last_user': last_registered_user  #Último registro 
        }
        
        return render(request, 'login_successful.html', context)
    
    except Register.DoesNotExist:
        #Manejo de error si usuario no existe -LGS
        print("Error: Usuario no encontrado en BD. Intentelo de nuevo") #Debug para usuario no encontrado -LGS
        messages.error(request, 'La cuenta no existe. Intentelo de nuevo')
        return redirect('home')
    
    except Exception as e:
        #Manejo de errores genéricos
        print(f"Error inesperado: {str(e)}")
        messages.error(request, 'Error al cargar la página. Intentelo de nuevo')
        return redirect('home')

#Vista para cierre de sesión -LGS
def logout_view(request):
    request.session.flush()  #Borra todos los datos de sesión al deslogearte -LGS
    
    return redirect('home') #Redirección a página principal -LGS

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
            messages.error(request, "No existe una cuenta con este correo. Intentelo de nuevo", extra_tags="password_reset")

    form = PasswordResetRequestForm() 
    return render(request, "password_reset_request.html", {"form": form})


#Vista para manejar la confirmación del restablecimiento de contraseña.
def password_reset_confirm(request, uidb64, token):    
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Register.objects.get(pk=uid)
        print(f"Usuario encontrado: {user.email}")  # Debug
        print(f"Token recibido: {token}")  # Debug
        print(f"Token en BD: {user.reset_token}")  # Debug
        print(f"Expiración: {user.reset_token_expiration}")  # Debug
    except Exception as e:
        print(f"Error decodificando: {str(e)}")
        user = None

    if user and validate_reset_token(user, token):
        if request.method == "POST":
            form = PasswordResetForm(request.POST)
            if form.is_valid():
                new_password = form.cleaned_data['new_password']
                
                # Actualiza la contraseña (CORREGIDO)
                user.passrd = make_password(new_password)
                user.reset_token = None
                user.reset_token_expiration = None
                user.save()
                
                print("Nueva contraseña:", new_password)  # Debug
                print("Hash guardado:", user.passrd)  # Debug
                
                messages.success(request, "¡Contraseña actualizada!")
                return redirect("password_reset_complete")
            else:
                messages.error(request, "Error en el formulario. Intentelo de nuevo")
        else:
            form = PasswordResetForm()
        
        return render(request, "password_reset_confirm.html", {"form": form, "username": user.name})
    else:
        messages.error(request, "Enlace inválido o expirado. Por favor intentelo de nuevo")
        return redirect("password_reset")

#funcion simple para renderizar el template que dice "correo enviado" -LGS
def password_reset_done(request):
    return render(request, "password_reset_done.html")

#funcion simple para renderizar el template que dice "cambio completado de contraseña"
def password_reset_complete(request):
    return render(request, "password_reset_complete.html")

#Función solo para ver el error 404 -Emix
def error404_view(request):
    return render(request, "temp_errors/404.html", status=404)
#Función nueva para función correcta de error 404 -Emix
def handling_404(request, exception):
    return render(request, "temp_errors/404.html", status=404)
#Función nueva para función correcta de error 500 -Emix
def handling_500(request):
    return render(request, "temp_errors/server-error-500.html")
def error_500_view(request):
#Puedes retornar directamente un template para el error 500
    return render(request, "temp_errors/server-error-500.html", status=500)
