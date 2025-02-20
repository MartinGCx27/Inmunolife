from django.views.generic import CreateView
from django.urls import reverse_lazy #Se agrega redirect de django -Emix
from django.contrib import messages #Se importa messages de django -Emix
from .models import Contactos
from .forms import FormContact, RegisterForm

from django.shortcuts import render, redirect #Se agrega redirect de django -Emix
from django.http import HttpRequest
from core.forms import FormContact, RegisterForm
from django.conf import settings #Se importa settings de la configuración  de django -Emix
from django.contrib.auth import login
from .models import User
from django.core.validators import validate_integer
from django.core.exceptions import ValidationError



class inmunolife_home(CreateView):
    model = Contactos
    form_class = FormContact
    template_name = 'index.html'
    success_url = reverse_lazy('home')
    
    def form_valid(self, form):
        messages.success(self.request, '¡Mensaje enviado con éxito!')
        return super().form_valid(form)
    def form_invalid(self, form):
        # Asegúra de mostrar los errores si el formulario es inválido
        return super().form_invalid(form)
    
# Función para registrar usuarios intento 3
def register_user(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            #login(request, user)  --> Inicia sesión automáticamente
            #return redirect("index")  # Redirige a la página principal
    else:
        form = RegisterForm()
    

    return render(request, "index.html")
# Función para registrar usuarios 2, -Emix
# def User(request):
#     RegistroUsuarioForm = User()
#     return render(request, 'index.html', {'form': RegistroUsuarioForm})

#     if request.method == 'POST':
#         RegistroUsuarioForm.save()
        
#         return redirect(reverse('home'+'?ok'))
#     else: 
#         return redirect(reverse('home'+'?error'))
# #     # Función para registrar usuarios -Emix
# def registro_view(request):
#     error = None
    
#     if request.method == 'POST':
#         try:
#             if len(cellphone_number) != 10:
#                 raise ValidationError("El número de celular debe tener 10 dígitos.")
#                 validate_integer(cellphone_number)
#         except ValidationError as e:
#             error = str(e)

#         name = request.POST.get('name')
#         lastname = request.POST.get('lastname')
#         second_lastname = request.POST.get('second_lastname')
#         email = request.POST.get('email')
#         cellphone_number = request.POST.get('cellphone_number')
#         password = request.POST.get('password')
        
#         if not all([name, lastname, email, cellphone_number, password]):
#             error = "Todos los campos marcados como obligatorios deben ser llenados."
#         else:
#             if User.objects.filter(email=email).exists():
#                 error = "Este correo electrónico ya está registrado."
#             elif User.objects.filter(cellphone_number=cellphone_number).exists():
#                 error = "Este número de celular ya está registrado."
#             else:
#                 User.objects.create(
#                     name=name,
#                     lastname=lastname,
#                     second_lastname=second_lastname,
#                     email=email,
#                     cellphone_number=cellphone_number,
#                     password=make_password(password),
#                     is_active=True,
#                 )
#                 return redirect('index.html') 
    
#     return render(request, 'index.html', {'error': error})

class FormContactView(HttpRequest):

    #Renderiza vista del formulario -LGS
    def index(request):
        contact = FormContact() 
        
        return render(request, "index.html", {"form":contact})
    
    #Valida la info que reciba del navedagor -LGS
    def procesar_formulario(request):
        contact = FormContact(request.POST)
        if contact.is_valid():
            contact.save()
            
            contact = FormContact()
            
        return render(request, 'index.html', {'form':contact, 'mensaje': 'OK'})

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
        
        