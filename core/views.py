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






# from django.shortcuts import render
# from django.views.generic import FormView
# from .forms import FormContact

# class inmunolife_home(FormView):
#     template_name = 'index.html'  
#     form_class = FormContact

#     def get_success_url(self):
#         # Redirige a la misma página después de que el formulario se haya enviado
#         return self.request.path_info  # Devuelve la URL actual

#     def form_valid(self, form):
#         # Puedes realizar alguna acción adicional al enviar el formulario, si es necesario
#         form.save()
#         # Mostrar un mensaje o agregar algo más si es necesario
#         return super().form_valid(form)

#     def form_invalid(self, form):
#         # Asegúrate de mostrar los errores si el formulario es inválido
#         return super().form_invalid(form)


# Create your views here.
# Home view
# def inmunolife_home(request):
#     return render(request, "index.html")


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
        
        