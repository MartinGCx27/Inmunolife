from django.shortcuts import render, redirect #Se agrega redirect de django -Emix
from django.http import HttpRequest
from core.forms import FormContact, RegisterForm
from django.contrib.auth.hashers import make_password
from django.conf import settings #Se importa settings de la configuración  de django -Emix
from django.contrib import messages #Se importa messages de django -Emix
from django.contrib.auth import login
from .models import User
from django.core.validators import validate_integer
from django.core.exceptions import ValidationError




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

# Create your views here.
# Home view
def inmunolife_home(request):
    return render(request, "index.html")


#Función para el captcha en index -Emix
def index_page(request):
    if request.method == 'POST':
        recaptcha_response = request.POST.get('g-recaptcha-response')
        
        data = {
            'secret': settings.RECAPTCHA_SECERET_KEY,
            'respone': recaptcha_response
        }
        verify_url = 'https://www.google.com/recaptcha/api.siteverify'
        response = request.post(verify_url, data=data)
        result = response.json()
        
        if result.get('success'):
            
            return redirect('success')
        
        else:
            messages.error(request, 'verificación del reCAPTCHA fallida. Por favor intentelo de nuevo')
            
    return render (request, 'index.html')
        
        