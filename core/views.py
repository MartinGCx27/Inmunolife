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
from django.contrib.auth.hashers import make_password



class inmunolife_home(CreateView):
    model = Contactos
    form_class = FormContact
    template_name = 'index.html'
    success_url = reverse_lazy('home')
    prefix = 'contact'

    def get_context_data(self, **kwargs):  #se agrega el get_context_data para maquetar ambos formularios -LGS
        context = super().get_context_data(**kwargs)
        context['register_form'] = RegisterForm(prefix="register")
        return context

    def form_valid(self, form):
        # Mensaje éxito contacto (tags: 'success contact')
        messages.success(self.request, '¡Mensaje de contacto enviado con éxito!', extra_tags="contact") #Se agrega el extra_tags para el FormContact para envio exitoso -LGS
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Error en el formulario de contacto', extra_tags="contact") #Se agrega el extra_tags para el FormContact para envio exitoso-LGS
        return super().form_invalid(form)  #Renderiza el template con el formulario inválido -LGS

#Funcion para registrar ahorá sí chila -Emix
def register_user(request):
    register_form = RegisterForm()
    if request.POST:
        register_form = RegisterForm(request.POST, prefix="register")
        if register_form.is_valid():
            user = register_form.save(commit=False)
            user.passrd = make_password(register_form.cleaned_data['passrd'])
            user.save()
            messages.add_message(request=request, level=messages.SUCCESS, message="¡Usuario registrado!", extra_tags="register")
            return redirect('home')
            
        else:
            messages.add_message(request=request, level=messages.ERROR, message="¡Usuario no registrado!", extra_tags="register")
            return redirect('home') 

        
# def register_user(request):
#     if request.method == "POST":
#         register_form = RegisterForm(request.POST, prefix="register")#Prefijo para dar nombre a a los elementos del Form register -LGS
#         if register_form.is_valid():
#             user = register_form.save(commit=False)
#             user.passrd = make_password(register_form.cleaned_data['passrd'])
#             user.save()
#             # Mensaje éxito registro (tags: 'success register')
#             messages.success(request, "¡Registro exitoso!", extra_tags="register")
#             return redirect("home")
#         else:
#             # Mensaje error registro (tags: 'error register')
#             messages.error(request, "Error en el registro", extra_tags="register")
#             contact_form = FormContact(prefix="contact")
#             #Si hay un error en ambos formularios los rederiza en index.html -LGS
#             return render(request, "index.html", {
#                 "form": contact_form,
#                 "register_form": register_form
#             })
#     return redirect("home") #redirecciona a la pagina principal, antes lo hacia a registro -LGS                                                                                                                                                                                                                                                                 


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