from django import forms
from .models import Contactos, Register

# formulario para contactanos -LGS
class FormContact(forms.ModelForm):
    class Meta:
        model = Contactos
        fields = ['name_contact', 'lastname_contact', 'phone_contact', 'email_contact', 'topic_contact', 'comments_contact']
        widgets = {
            'name_contact': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tu Nombre'}),
            'lastname_contact': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tu Apellido'}),
            'phone_contact': forms.NumberInput(attrs={'class': 'form-control ', 'placeholder': 'Tu Telefono'}),
            'email_contact': forms.EmailInput(attrs={'class': 'form-control ','placeholder': 'Tu correo personal'}),
            'topic_contact': forms.Select(attrs={'class': 'dropdown-item'}),
            'comments_contact': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Inserta tus comentarios', 'rows': 6}),
        }
        
        

# Clase para registrar usuarios
class RegisterForm(forms.ModelForm):
    class Meta:
        model = Register
        fields = [
            'name',
            'last_name',
            'second_lastname',
            'email',
            'passrd',
            'cellphone'
            ]
        