from django.views.generic import CreateView
from django.urls import reverse_lazy #Se agrega redirect de django -Emix
from django.contrib import messages
from django.http import HttpRequest
from .models import Contactos
from .forms import FormContact, RegisterForm
from django.contrib.auth.hashers import make_password
from django.conf import settings #Se importa settings de la configuración  de django -Emix
from django.contrib import messages #Se importa messages de django -Emix
from django.contrib.auth import login
from .models import User
from django.core.validators import validate_integer
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect



# Función para registrar usuarios 
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
class inmunolife_home(CreateView):
    model = 'Contactos'
    form_class = FormContact
    template_name = 'index.html'
    success_url = reverse_lazy('home')
    
    def form_valid(self, form):
        messages.success(self.request, '¡Mensaje enviado con éxito!')
        return super().form_valid(form)
    def form_invalid(self, form):
        # Asegúra de mostrar los errores si el formulario es inválido
        return super().form_invalid(form)



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
# def inmunolife_home(request):
#     return render(request, "index.html")


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
        
        