from django.shortcuts import render
from django.http import HttpRequest
from core.forms import FormContact

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