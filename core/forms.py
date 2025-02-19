from django import forms
from .models import Contactos, Register

class FormContact(forms.ModelForm):
    class Meta:
        model = Contactos
        fields = '__all__'
        

# Clase para registrar usuarios
class RegisterForm(forms.ModelForm):
    class Meta:
        model = Register
        fields = [
            'name',
            'second_lastname'
            ]
        