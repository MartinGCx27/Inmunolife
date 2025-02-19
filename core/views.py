from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Contactos
from .forms import FormContact

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
#     contact_form = FormContact()
#     return render(request, "index.html")