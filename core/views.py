import pdb
from django.core.validators import validate_integer
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from django.urls import reverse_lazy 
from django.contrib import messages 
from django.conf import settings
from .models import Contactos, Register  #no se estaban importando el modelo Register, se agrega -LGS
from .forms import FormContact, RegisterForm, LoginForm



class inmunolife_home(CreateView):
    model = Contactos
    form_class = FormContact
    template_name = 'index.html'
    success_url = reverse_lazy('home')
    
    def form_valid(self, form):
        messages.success(self.request, '¡Mensaje enviado con éxito!')
        return super().form_valid(form)
    def form_invalid(self, form):
        messages.error(self.request, 'No se pudo enviar tu formulario. Por favor, revisa los campos e inténtalo de nuevo.')
        return super().form_invalid(form)

#Funcion para registrar ahorá sí chila -Emix
def register_user(request):
    contact_form = FormContact()
    if request.method == "POST":
        register = RegisterForm(request.POST, prefix="register")
        # Obtenemos las contraseñas
        password = request.POST.get("passrd")
        confirm_password = request.POST.get("confirm_passrd")
        # Validamos si las contraseñas coinciden
        if password != confirm_password:
            messages.error(request, "Las contraseñas no coinciden.", extra_tags="register")
        elif register.is_valid():
            register.save()
            messages.success(request, "¡Registro de usuario exitoso!", extra_tags="register")
            return redirect("register_user")
        else:
            messages.error(request, "Ha ocurrido un error en el registro. Revisa los datos ingresados.", extra_tags="register")
    else:
        register = RegisterForm(prefix="register")
    
    return render(request, "index.html", {"form1": register, "form2": contact_form})

#Función para el captcha en index -Emix
def index_page(request):
    if request.method == 'POST':
        recaptcha_response = request.POST.get('g-recaptcha-response')
        
        data = {
            'secret': settings.RECAPTCHA_SECRET_KEY,
            'response': recaptcha_response
        }
        verify_url = 'https://www.google.com/recaptcha/api.siteverify'
        response = request.post(verify_url, data=data)
        result = response.json()
        
        if result.get('success'):
            
            return redirect('success')
        
        else:
            messages.error(request, 'verificación del reCAPTCHA fallida. Por favor intentelo de nuevo')
            
    return render (request, 'index.html')

#Función para el Login -Emix
#@login_required
def login(request):
    last_user = Register.objects.order_by('-id').first()  #para pruebgas de starter page muestre el nombre de usuario -LGS
     #print("Último usuario registrado:", last_user)
    return render(request, 'starter-page.html', {'last_user': last_user})

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
